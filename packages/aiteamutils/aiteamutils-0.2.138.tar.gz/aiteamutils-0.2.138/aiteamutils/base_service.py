#기본 라이브러리
from fastapi import Request
from typing import TypeVar, Generic, Type, Dict, Any, Union, List, Optional, Literal
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from ulid import ULID

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
        
        try:
            # 파일 데이터 분리
            entity_data_copy = entity_data.copy()
            separated_files = {}
            
            # extra_data 내의 파일 필드 분리
            if 'extra_data' in entity_data_copy and isinstance(entity_data_copy['extra_data'], dict):
                extra_data = entity_data_copy['extra_data'].copy()
                file_fields = {k: v for k, v in extra_data.items() if k.endswith('_files')}
                
                if file_fields and not storage_dir:
                    raise CustomException(
                        ErrorCode.INVALID_INPUT,
                        detail="storage_dir is required for file upload",
                        source_function=f"base_service.{self.__class__.__name__}.create.file_fields"
                    )
                
                # 파일 필드 분리 및 제거
                for field_name, files in file_fields.items():
                    if files:
                        separated_files[field_name] = files
                        # extra_data에서 파일 필드 제거
                        del extra_data[field_name]
                
                entity_data_copy['extra_data'] = extra_data

            async with self.db_session.begin():
                # 고유 검사 수행
                if unique_check:
                    await validate_unique_fields(self.db_session, unique_check, find_value=True)
                # 외래 키 검사 수행
                if fk_check:
                    await validate_unique_fields(self.db_session, fk_check, find_value=False)
                
                # 엔티티 생성
                result = await self.repository.create(
                    entity_data=entity_data_copy,
                    exclude_entities=exclude_entities
                )
                
                # 파일 처리 및 저장
                file_infos = {}
                if separated_files:
                    from .files import FileHandler
                    for field_name, files in separated_files.items():
                        saved_files = await FileHandler.save_files(
                            files=files,
                            storage_dir=storage_dir,
                            entity_name=self.model.__tablename__,
                            entity_ulid=result.ulid,
                            db_session=self.db_session
                        )
                        file_infos[field_name] = saved_files
                        
                        # extra_data 업데이트
                        if not hasattr(result, 'extra_data'):
                            result.extra_data = {}
                        if not result.extra_data:
                            result.extra_data = {}
                            
                        result.extra_data[field_name] = [
                            {
                                'original_name': f['original_name'],
                                'storage_path': f['storage_path'],
                                'mime_type': f['mime_type'],
                                'size': f['size'],
                                'checksum': f['checksum']
                            } for f in saved_files
                        ]
                    
                    # extra_data 업데이트된 엔티티 저장
                    await self.db_session.flush()

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
            # 파일 저장 실패 시 저장된 파일들 삭제
            if 'file_infos' in locals():
                for file_list in file_infos.values():
                    for file_info in file_list:
                        from .files import FileHandler
                        await FileHandler.delete_files(file_info["storage_path"])
            raise e
        except Exception as e:
            # 다른 예외 처리
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
        token_settings: Dict[str, Any] | None = None
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

                result = await self.repository.update(
                    entity_data=entity_data,
                    conditions=conditions,
                    exclude_entities=exclude_entities
                )

                if response_model:
                    return process_response(result, response_model)
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
        token_settings: Dict[str, Any] | None = None
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

