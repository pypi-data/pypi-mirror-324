#기본 라이브러리
from fastapi import Request
from typing import TypeVar, Generic, Type, Dict, Any, Union, List, Optional, Literal, Tuple
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from ulid import ULID
from sqlalchemy import text

#패키지 라이브러리
from .exceptions import ErrorCode, CustomException
from .base_repository import BaseRepository
from .database import (
    process_response,
    validate_unique_fields
)
from .security import hash_password, verify_jwt_token, verify_role_permission
ModelType = TypeVar("ModelType", bound=DeclarativeBase)

class BaseService(Generic[ModelType]):
    ##################
    # 초기화 영역 #
    ##################
    def __init__(
            self,
            model: Type[ModelType],
            repository: BaseRepository[ModelType],
            db_session: AsyncSession,
            additional_models: Dict[str, Type[DeclarativeBase]] = None,
    ):
        self.model = model
        self.repository = repository
        self.db_session = db_session
        self.additional_models = additional_models or {},
    
    #######################
    # 입력 및 수정, 삭제 #
    #######################
    async def _process_files(
        self,
        entity_data: Dict[str, Any],
        entity_result: Any,
        storage_dir: str,
        operation: Literal["create", "update", "delete"] = "create"
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """파일 처리를 위한 내부 메서드
        
        Args:
            entity_data (Dict[str, Any]): 엔티티 데이터
            entity_result (Any): 생성/수정된 엔티티 결과
            storage_dir (str): 저장 디렉토리 경로
            operation (str): 수행할 작업 유형 ("create", "update", "delete")
            
        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: (처리된 엔티티 데이터, 파일 정보)
        """
        try:
            entity_data_copy = entity_data.copy()
            file_infos = {}
            
            # 파일 데이터 분리
            separated_files = {}
            if operation != "delete" and 'extra_data' in entity_data_copy and isinstance(entity_data_copy['extra_data'], dict):
                extra_data = entity_data_copy['extra_data'].copy()
                file_fields = {k: v for k, v in extra_data.items() if k.endswith('_files')}
                
                if file_fields and not storage_dir:
                    raise CustomException(
                        ErrorCode.INVALID_INPUT,
                        detail="storage_dir is required for file upload",
                        source_function=f"{self.__class__.__name__}._process_files"
                    )
                
                # 파일 필드 분리 및 제거
                for field_name, files in file_fields.items():
                    if files:
                        separated_files[field_name] = files
                        del extra_data[field_name]
                
                entity_data_copy['extra_data'] = extra_data

            # 기존 파일 삭제 (update 또는 delete 작업 시)
            if operation in ["update", "delete"]:
                from .files import FileHandler
                # files 테이블에서 기존 파일 정보 조회
                existing_files = await self.db_session.execute(
                    text("""
                        SELECT storage_path 
                        FROM files 
                        WHERE entity_name = :entity_name 
                        AND entity_ulid = :entity_ulid
                    """),
                    {
                        "entity_name": self.model.__tablename__,
                        "entity_ulid": entity_result.ulid
                    }
                )
                existing_files = existing_files.fetchall()
                
                # 기존 파일 삭제
                for file_info in existing_files:
                    await FileHandler.delete_files(file_info[0])
                
                # files 테이블에서 레코드 삭제
                await self.db_session.execute(
                    text("""
                        DELETE FROM files 
                        WHERE entity_name = :entity_name 
                        AND entity_ulid = :entity_ulid
                    """),
                    {
                        "entity_name": self.model.__tablename__,
                        "entity_ulid": entity_result.ulid
                    }
                )

            # 새 파일 저장 (create 또는 update 작업 시)
            if operation != "delete" and separated_files:
                from .files import FileHandler
                for field_name, files in separated_files.items():
                    saved_files = await FileHandler.save_files(
                        files=files,
                        storage_dir=storage_dir,
                        entity_name=self.model.__tablename__,
                        entity_ulid=entity_result.ulid,
                        db_session=self.db_session,
                        column_name=field_name.replace('_files', '')
                    )
                    file_infos[field_name] = saved_files
                    
                    # extra_data 업데이트 - 파일 정보 캐싱
                    if not hasattr(entity_result, 'extra_data'):
                        entity_result.extra_data = {}
                    if not entity_result.extra_data:
                        entity_result.extra_data = {}
                        
                    entity_result.extra_data[field_name] = [
                        {
                            'original_name': f['original_name'],
                            'storage_path': f['storage_path'],
                            'mime_type': f['mime_type'],
                            'size': f['size'],
                            'checksum': f['checksum'],
                            'column_name': f['column_name']
                        } for f in saved_files
                    ]
                
                # extra_data 업데이트된 엔티티 저장
                await self.db_session.flush()

            return entity_data_copy, file_infos

        except CustomException as e:
            if file_infos:
                from .files import FileHandler
                for file_list in file_infos.values():
                    for file_info in file_list:
                        await FileHandler.delete_files(file_info["storage_path"])
            raise CustomException(
                e.error_code,
                detail=e.detail,
                source_function=f"{self.__class__.__name__}._process_files",
                original_error=e
            )
        except Exception as e:
            if file_infos:
                from .files import FileHandler
                for file_list in file_infos.values():
                    for file_info in file_list:
                        await FileHandler.delete_files(file_info["storage_path"])
            raise CustomException(
                ErrorCode.FILE_SYSTEM_ERROR,
                detail=str(e),
                source_function=f"{self.__class__.__name__}._process_files",
                original_error=e
            )

    async def create(
        self,
        request: Request,
        entity_data: Dict[str, Any],
        response_model: Any = None,
        exclude_entities: List[str] | None = None,
        unique_check: List[Dict[str, Any]] | None = None,
        fk_check: List[Dict[str, Any]] | None = None,
        org_ulid_position: str = "organization_ulid",
        role_permission: str | None = None,
        token_settings: Dict[str, Any] | None = None,
        storage_dir: str | None = None
    ) -> ModelType:
        try:
            if role_permission:
                permission_result = await verify_role_permission(
                    request=request,
                    role_permission=role_permission,
                    token_settings=token_settings,
                    org_ulid_position=org_ulid_position
                )
            
                if not permission_result:
                    raise CustomException(
                        ErrorCode.FORBIDDEN,
                        detail=f"{role_permission}",
                        source_function=f"base_service.{self.__class__.__name__}.create.permission_result"
                    )

            async with self.db_session.begin():
                # 고유 검사 수행
                if unique_check:
                    await validate_unique_fields(self.db_session, unique_check, find_value=True)
                # 외래 키 검사 수행
                if fk_check:
                    await validate_unique_fields(self.db_session, fk_check, find_value=False)
                
                # 파일 데이터 분리를 위한 임시 엔티티 생성
                temp_entity = type('TempEntity', (), {'ulid': str(ULID())})()
                
                # 파일 데이터 분리
                entity_data_copy, _ = await self._process_files(
                    entity_data=entity_data,
                    entity_result=temp_entity,
                    storage_dir=storage_dir,
                    operation="create"
                )
                
                # 엔티티 생성 (파일 데이터가 제거된 상태)
                result = await self.repository.create(
                    entity_data=entity_data_copy,
                    exclude_entities=exclude_entities
                )
                
                # 실제 파일 처리
                _, file_infos = await self._process_files(
                    entity_data=entity_data,
                    entity_result=result,
                    storage_dir=storage_dir,
                    operation="create"
                )

                # 결과 반환
                if response_model:
                    processed_result = process_response(result, response_model)
                    # 파일 정보 추가
                    for key, value in file_infos.items():
                        processed_result[key] = value
                    return processed_result
                else:
                    return result

        except CustomException as e:
            raise e
        except Exception as e:
            raise CustomException(
                ErrorCode.INTERNAL_ERROR,
                detail=str(e),
                source_function=f"base_service.{self.__class__.__name__}.create",
                original_error=e
            )

    async def update(
        self,
        request: Request,
        ulid: str | None = None,
        entity_data: Dict[str, Any] | None = None,
        conditions: Dict[str, Any] | None = None,
        unique_check: List[Dict[str, Any]] | None = None,
        exclude_entities: List[str] | None = None,
        response_model: Any = None,
        org_ulid_position: str = "organization_ulid",
        role_permission: str = "update",
        token_settings: Dict[str, Any] | None = None,
        storage_dir: str | None = None
    ) -> ModelType:
        try:
            async with self.db_session.begin():
                # 고유 검사 수행
                if unique_check:
                    await validate_unique_fields(self.db_session, unique_check, find_value=True)

                if not ulid and not conditions:
                    raise CustomException(
                        ErrorCode.INVALID_INPUT,
                        detail="Either 'ulid' or 'conditions' must be provided.",
                        source_function=f"base_service.{self.__class__.__name__}.update.ulid_or_conditions"
                    )

                # ulid로 조건 생성
                if ulid:
                    if not ULID.from_str(ulid):
                        raise CustomException(
                            ErrorCode.VALIDATION_ERROR,
                            detail=ulid,
                            source_function=f"base_service.{self.__class__.__name__}.update.ulid_or_conditions"
                        )
                    
                    conditions = {"ulid": ulid}

                # 기존 엔티티 조회
                existing_entity = await self.repository.get(conditions=conditions)
                if not existing_entity:
                    raise CustomException(
                        ErrorCode.NOT_FOUND,
                        detail=str(ulid or conditions),
                        source_function=f"base_service.{self.__class__.__name__}.update.get_entity"
                    )

                # 파일 데이터 분리
                entity_data_copy, _ = await self._process_files(
                    entity_data=entity_data,
                    entity_result=existing_entity,
                    storage_dir=storage_dir,
                    operation="update"
                )

                # 엔티티 수정 (파일 데이터가 제거된 상태)
                result = await self.repository.update(
                    entity_data=entity_data_copy,
                    conditions=conditions,
                    exclude_entities=exclude_entities
                )

                # 실제 파일 처리
                _, file_infos = await self._process_files(
                    entity_data=entity_data,
                    entity_result=result,
                    storage_dir=storage_dir,
                    operation="update"
                )

                if response_model:
                    processed_result = process_response(result, response_model)
                    # 파일 정보 추가
                    for key, value in file_infos.items():
                        processed_result[key] = value
                    return processed_result
                else:
                    return result

        except CustomException as e:
            raise e
        except Exception as e:
            raise CustomException(
                ErrorCode.INTERNAL_ERROR,
                detail=str(e),
                source_function=f"base_service.{self.__class__.__name__}.update",
                original_error=e
            )

    async def delete(
        self,
        request: Request,
        ulid: str | None = None,
        conditions: Dict[str, Any] | None = None,
        org_ulid_position: str = "organization_ulid",
        role_permission: str = "delete",
        token_settings: Dict[str, Any] | None = None,
        storage_dir: str | None = None
    ) -> bool:
        try:
            if not ULID.from_str(ulid):
                raise CustomException(
                    ErrorCode.VALIDATION_ERROR,
                    detail=ulid,
                    source_function=f"base_service.{self.__class__.__name__}.delete.ulid_validation"
                )
            
            if not ulid and not conditions:
                raise CustomException(
                    ErrorCode.INVALID_INPUT,
                    detail="Either 'ulid' or 'conditions' must be provided.",
                    source_function=f"base_service.{self.__class__.__name__}.delete.ulid_or_conditions"
                )

            # ulid로 조건 생성
            if ulid:
                conditions = {"ulid": ulid}

            conditions["is_deleted"] = False

            # 엔티티 조회 (파일 삭제를 위해)
            entity = await self.repository.get(conditions=conditions)
            if not entity:
                return False

            # 파일 처리 (삭제)
            _, _ = await self._process_files(
                entity_data={},
                entity_result=entity,
                storage_dir=storage_dir,
                operation="delete"
            )

            return await self.repository.delete(
                conditions=conditions
            )
        except CustomException as e:
            raise e
        except Exception as e:
            raise CustomException(
                ErrorCode.INTERNAL_ERROR,
                detail=str(e),
                source_function=f"base_service.{self.__class__.__name__}.delete",
                original_error=e
            )

    #########################
    # 조회 및 검색 메서드 #
    #########################
    async def list(
        self,
        request: Request,
        skip: int = 0,
        limit: int = 100,
        filters: List[Dict[str, Any]] | None = None,
        org_ulid_position: str = "organization_ulid",
        role_permission: str | None = None,
        response_model: Any = None,
        explicit_joins: Optional[List[Any]] = None,
        loading_joins: Optional[List[Any]] = None,
        order: Optional[str] = None,
        token_settings: Dict[str, Any] | None = None
    ) -> List[Dict[str, Any]]:
        filters = list(filters) if filters is not None else []

        if role_permission:
            permission_result = await verify_role_permission(
                request=request,
                role_permission=role_permission,
                token_settings=token_settings,
                org_ulid_position=org_ulid_position
            )

            if permission_result and isinstance(permission_result, dict):
                filters.append(permission_result)

        try:
            if order is None:
                order = "created_at|desc"

                order_by = order.split("|")
                order = [{"field": order_by[0], "direction": order_by[1]}]

            entities = await self.repository.list(
                skip=skip,
                limit=limit,
                filters=filters,
                explicit_joins=explicit_joins,
                loading_joins=loading_joins,
                order=order
            )
            return [process_response(entity, response_model) for entity in entities]
        
        except CustomException as e:
            raise e
        except Exception as e:
            raise CustomException(
                ErrorCode.INTERNAL_ERROR,
                source_function=f"base_service.{self.__class__.__name__}.list",
                original_error=e
            )
        
    async def get(
        self,
        request: Request,
        ulid: str,
        model_name: str | None = None,
        response_model: Any = None,
        conditions: Dict[str, Any] | None = None,
        explicit_joins: Optional[List[Any]] = None,
        loading_joins: Optional[List[Any]] = None,
        org_ulid_position: str = "organization_ulid",
        role_permission: str = "get",
        token_settings: Dict[str, Any] | None = None
    ):
        try:
            if not ulid and not conditions:
                raise CustomException(
                    ErrorCode.INVALID_INPUT,
                    detail="Either 'ulid' or 'conditions' must be provided.",
                    source_function=f"base_service.{self.__class__.__name__}.get.ulid_or_conditions"
                )

            # ulid로 조건 생성
            if ulid:
                if not ULID.from_str(ulid):
                    raise CustomException(
                        ErrorCode.VALIDATION_ERROR,
                        detail=ulid,
                        source_function=f"base_service.{self.__class__.__name__}.get.ulid_validation"
                    )
                
                conditions = {"ulid": ulid}
            
            entity = await self.repository.get(
                conditions=conditions,
                explicit_joins=explicit_joins,
                loading_joins=loading_joins
            )
            return process_response(entity, response_model)

        except CustomException as e:
            raise e
        except Exception as e:
            raise CustomException(
                ErrorCode.INTERNAL_ERROR,
                detail=str(e),
                source_function=f"base_service.{self.__class__.__name__}.get",
                original_error=e
            )

