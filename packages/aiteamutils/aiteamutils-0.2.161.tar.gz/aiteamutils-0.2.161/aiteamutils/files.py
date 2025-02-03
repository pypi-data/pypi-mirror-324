import os
import hashlib
import aiofiles
from datetime import datetime, timezone
from typing import BinaryIO, Dict, Any, List, Tuple, Union
from pathlib import Path
from mimetypes import guess_type
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from ulid import ULID
import logging

from .exceptions import ErrorCode, CustomException
from .base_model import BaseFileModel

logger = logging.getLogger(__name__)

class FileHandler:
    """파일 처리를 위한 핵심 기능 제공 클래스"""
    
    @staticmethod
    def _create_directory(directory: str) -> None:
        """디렉토리가 없는 경우 생성"""
        try:
            logger.info(f"[디렉토리 생성 시도] {directory}")
            if os.path.exists(directory):
                logger.info(f"[디렉토리 이미 존재] {directory}")
                return
                
            os.makedirs(directory, exist_ok=True)
            logger.info(f"[디렉토리 생성 완료] {directory}")
            
            # 권한 확인
            if not os.access(directory, os.W_OK):
                logger.error(f"[권한 에러] 디렉토리에 쓰기 권한 없음: {directory}")
                raise CustomException(
                    ErrorCode.FILE_SYSTEM_ERROR,
                    detail=f"{directory}|No write permission",
                    source_function="FileHandler._create_directory"
                )
                
        except Exception as e:
            logger.error(f"[디렉토리 생성 실패] {directory}: {str(e)}")
            raise CustomException(
                ErrorCode.FILE_SYSTEM_ERROR,
                detail=f"{directory}|{str(e)}",
                source_function="FileHandler._create_directory",
                original_error=e
            )

    @staticmethod
    def _split_mime_type(mime_type: str) -> Tuple[str, str]:
        """MIME 타입을 주 타입과 부 타입으로 분리
        
        Args:
            mime_type (str): MIME 타입 문자열 (예: "image/jpeg")
            
        Returns:
            Tuple[str, str]: (주 타입, 부 타입) 튜플
        """
        try:
            if not mime_type or '/' not in mime_type:
                return 'application', 'octet-stream'
            main_type, sub_type = mime_type.split('/', 1)
            return main_type.lower(), sub_type.lower()
        except Exception as e:
            logger.error(f"[MIME 타입 분리 실패] {mime_type}: {str(e)}")
            return 'application', 'octet-stream'

    @staticmethod
    async def _calculate_checksum(file: BinaryIO) -> str:
        """파일의 SHA-256 체크섬 계산
        
        Args:
            file (BinaryIO): 체크섬을 계산할 파일 객체
            
        Returns:
            str: 계산된 체크섬 값
        """
        try:
            sha256_hash = hashlib.sha256()
            current_position = file.tell()
            file.seek(0)
            
            for chunk in iter(lambda: file.read(4096), b""):
                sha256_hash.update(chunk)
            
            file.seek(current_position)
            return sha256_hash.hexdigest()
        except Exception as e:
            raise CustomException(
                ErrorCode.FILE_SYSTEM_ERROR,
                detail="checksum calculation failed",
                source_function="FileHandler._calculate_checksum",
                original_error=e
            )

    @staticmethod
    def _get_mime_type(filename: str) -> str:
        """파일의 MIME 타입 추측
        
        Args:
            filename (str): MIME 타입을 추측할 파일명
            
        Returns:
            str: 추측된 MIME 타입
        """
        mime_type, _ = guess_type(filename)
        return mime_type or "application/octet-stream"

    @staticmethod
    async def _save_file(
        file: BinaryIO,
        original_name: str,
        storage_dir: str,
        entity_name: str,
        entity_ulid: str
    ) -> Dict[str, Any]:
        """파일을 저장하고 메타데이터 반환"""
        try:
            logger.info(f"[파일 저장 시작] 원본 파일명: {original_name}, 저장 경로: {storage_dir}")
            
            # 저장 디렉토리 생성
            FileHandler._create_directory(storage_dir)
            
            # 파일 메타데이터 준비
            file_ext = os.path.splitext(original_name)[1]
            storage_filename = f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{entity_ulid}{file_ext}"
            storage_path = os.path.join(storage_dir, storage_filename)
            logger.info(f"[저장 파일명] {storage_filename}")
            
            # 파일 저장
            current_position = file.tell()
            file.seek(0)
            
            try:
                async with aiofiles.open(storage_path, 'wb') as f:
                    while chunk := file.read(8192):
                        await f.write(chunk)
                logger.info(f"[파일 쓰기 완료] {storage_path}")
            except Exception as e:
                logger.error(f"[파일 쓰기 실패] {storage_path}: {str(e)}")
                raise
            
            # 체크섬 계산
            file.seek(0)
            checksum = await FileHandler._calculate_checksum(file)
            logger.info(f"[체크섬 계산 완료] {checksum}")
            
            # 파일 포인터 복구
            file.seek(current_position)
            
            # MIME 타입 처리
            mime_type = FileHandler._get_mime_type(original_name)
            mime_type_main, mime_type_sub = FileHandler._split_mime_type(mime_type)
            logger.info(f"[MIME 타입 분리] {mime_type} -> {mime_type_main}/{mime_type_sub}")
            
            file_info = {
                "original_name": original_name,
                "storage_path": storage_path,
                "mime_type": mime_type,
                "mime_type_main": mime_type_main,
                "mime_type_sub": mime_type_sub,
                "size": os.path.getsize(storage_path),
                "checksum": checksum,
                "entity_name": entity_name,
                "entity_ulid": entity_ulid
            }
            logger.info(f"[파일 정보] {file_info}")
            return file_info
            
        except CustomException as e:
            logger.error(f"[CustomException 발생] {e.error_code}: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"[파일 저장 실패] {str(e)}")
            raise CustomException(
                ErrorCode.FILE_SYSTEM_ERROR,
                detail=f"{storage_path}|{str(e)}",
                source_function="FileHandler._save_file",
                original_error=e
            )

    @staticmethod
    async def save_files(
        files: Union[Tuple[BinaryIO, str], List[Tuple[BinaryIO, str]]],
        storage_dir: str,
        entity_name: str,
        entity_ulid: str,
        db_session: AsyncSession,
        column_name: str = None
    ) -> List[Dict[str, Any]]:
        """파일(들)을 저장하고 메타데이터 반환"""
        logger.info(f"[다중 파일 저장 시작] storage_dir: {storage_dir}, entity_name: {entity_name}")
        logger.info(f"[파일 데이터 타입] files type: {type(files)}")
        if isinstance(files, list):
            logger.info(f"[파일 리스트 내용] {[(type(f[0]), f[1]) for f in files]}")
        else:
            logger.info(f"[단일 파일 내용] {(type(files[0]), files[1])}")
        
        file_infos = []
        # 단일 파일인 경우 리스트로 변환
        files_list = [files] if isinstance(files, tuple) else files
        logger.info(f"[처리할 파일 수] {len(files_list)}")
        
        for file, original_name in files_list:
            try:
                logger.info(f"[개별 파일 처리 시작] {original_name}")
                logger.info(f"[파일 객체 정보] type: {type(file)}, seekable: {file.seekable()}, readable: {file.readable()}")
                
                # 파일 저장 및 메타데이터 생성
                file_info = await FileHandler._save_file(
                    file=file,
                    original_name=original_name,
                    storage_dir=storage_dir,
                    entity_name=entity_name,
                    entity_ulid=entity_ulid
                )
                
                # DB에 파일 정보 저장
                try:
                    logger.info(f"[DB 저장 시작] {original_name}")
                    file_ulid = str(ULID())
                    logger.info(f"[생성된 파일 ULID] {file_ulid}")
                    
                    now = datetime.now(timezone.utc)
                    result = await db_session.execute(
                        text("""
                            INSERT INTO files (
                                ulid, entity_name, entity_ulid, original_name, storage_path,
                                mime_type, mime_type_main, mime_type_sub, size, checksum, 
                                column_name, created_at, updated_at, is_deleted
                            ) VALUES (
                                :ulid, :entity_name, :entity_ulid, :original_name, :storage_path,
                                :mime_type, :mime_type_main, :mime_type_sub, :size, :checksum,
                                :column_name, :created_at, :updated_at, :is_deleted
                            ) RETURNING *
                        """),
                        {
                            "ulid": file_ulid,
                            "entity_name": entity_name,
                            "entity_ulid": entity_ulid,
                            "original_name": file_info["original_name"],
                            "storage_path": file_info["storage_path"],
                            "mime_type": file_info["mime_type"],
                            "mime_type_main": file_info["mime_type_main"],
                            "mime_type_sub": file_info["mime_type_sub"],
                            "size": file_info["size"],
                            "checksum": file_info["checksum"],
                            "column_name": column_name,
                            "created_at": now,
                            "updated_at": now,
                            "is_deleted": False
                        }
                    )
                    
                    row = result.fetchone()
                    db_file_info = {
                        "ulid": row.ulid,
                        "entity_name": row.entity_name,
                        "entity_ulid": row.entity_ulid,
                        "original_name": row.original_name,
                        "storage_path": row.storage_path,
                        "mime_type": row.mime_type,
                        "mime_type_main": row.mime_type_main,
                        "mime_type_sub": row.mime_type_sub,
                        "size": row.size,
                        "checksum": row.checksum,
                        "column_name": row.column_name,
                        "created_at": row.created_at,
                        "updated_at": row.updated_at,
                        "is_deleted": row.is_deleted
                    }
                    file_infos.append(db_file_info)
                    logger.info(f"[DB 저장 완료] {original_name}, ulid: {db_file_info['ulid']}")
                    
                except Exception as e:
                    logger.error(f"[DB 저장 실패] {original_name}: {str(e)}")
                    # 파일 삭제 시도
                    try:
                        if "storage_path" in file_info:
                            await FileHandler.delete_files(file_info["storage_path"])
                            logger.info(f"[저장 실패로 인한 파일 삭제] {file_info['storage_path']}")
                    except Exception as del_e:
                        logger.error(f"[파일 삭제 실패] {str(del_e)}")
                    raise
            except Exception as e:
                logger.error(f"[파일 처리 실패] {original_name}: {str(e)}")
                raise
        
        logger.info(f"[다중 파일 저장 완료] 성공: {len(file_infos)}개")
        return file_infos

    @staticmethod
    async def delete_files(storage_paths: Union[str, List[str]]) -> None:
        """파일(들) 삭제
        
        Args:
            storage_paths: 단일 파일 경로 또는 파일 경로 리스트
        """
        paths_list = [storage_paths] if isinstance(storage_paths, str) else storage_paths
        for storage_path in paths_list:
            await FileHandler._delete_file(storage_path)

    @staticmethod
    async def _delete_file(storage_path: str) -> None:
        """파일 삭제 (내부 사용)
        
        Args:
            storage_path (str): 삭제할 파일 경로
        """
        try:
            if os.path.exists(storage_path):
                os.remove(storage_path)
        except Exception as e:
            raise CustomException(
                ErrorCode.FILE_SYSTEM_ERROR,
                detail=str(storage_path),
                source_function="FileHandler._delete_file",
                original_error=e
            )

    @staticmethod
    async def read_file(storage_path: str) -> BinaryIO:
        """파일 읽기
        
        Args:
            storage_path (str): 읽을 파일 경로
            
        Returns:
            BinaryIO: 파일 객체
        """
        try:
            if not os.path.exists(storage_path):
                raise CustomException(
                    ErrorCode.FILE_NOT_FOUND,
                    detail=str(storage_path),
                    source_function="FileHandler.read_file"
                )
            
            return open(storage_path, 'rb')
        except CustomException as e:
            raise e
        except Exception as e:
            raise CustomException(
                ErrorCode.FILE_SYSTEM_ERROR,
                detail=str(storage_path),
                source_function="FileHandler.read_file",
                original_error=e
            ) 