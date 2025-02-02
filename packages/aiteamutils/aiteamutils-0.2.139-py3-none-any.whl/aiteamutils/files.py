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

from .exceptions import ErrorCode, CustomException

class FileHandler:
    """파일 처리를 위한 핵심 기능 제공 클래스"""
    
    @staticmethod
    def _create_directory(directory: str) -> None:
        """디렉토리가 없는 경우 생성
        
        Args:
            directory (str): 생성할 디렉토리 경로
        """
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            raise CustomException(
                ErrorCode.FILE_SYSTEM_ERROR,
                detail=str(directory),
                source_function="FileHandler._create_directory",
                original_error=e
            )

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
        """파일을 저장하고 메타데이터 반환 (내부 사용)
        
        Args:
            file (BinaryIO): 저장할 파일 객체
            original_name (str): 원본 파일명
            storage_dir (str): 저장 디렉토리 경로
            entity_name (str): 엔티티 이름
            entity_ulid (str): 엔티티 ULID
            
        Returns:
            Dict[str, Any]: 저장된 파일의 메타데이터
        """
        try:
            # 저장 디렉토리 생성
            FileHandler._create_directory(storage_dir)
            
            # 파일 메타데이터 준비
            file_ext = os.path.splitext(original_name)[1]
            storage_filename = f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{entity_ulid}{file_ext}"
            storage_path = os.path.join(storage_dir, storage_filename)
            
            # 파일 저장
            current_position = file.tell()
            file.seek(0)
            
            async with aiofiles.open(storage_path, 'wb') as f:
                while chunk := file.read(8192):
                    await f.write(chunk)
            
            # 체크섬 계산
            file.seek(0)
            checksum = await FileHandler._calculate_checksum(file)
            
            # 파일 포인터 복구
            file.seek(current_position)
            
            return {
                "original_name": original_name,
                "storage_path": storage_path,
                "mime_type": FileHandler._get_mime_type(original_name),
                "size": os.path.getsize(storage_path),
                "checksum": checksum,
                "entity_name": entity_name,
                "entity_ulid": entity_ulid
            }
        except CustomException as e:
            raise e
        except Exception as e:
            raise CustomException(
                ErrorCode.FILE_SYSTEM_ERROR,
                detail=str(storage_path),
                source_function="FileHandler._save_file",
                original_error=e
            )

    @staticmethod
    async def save_files(
        files: Union[Tuple[BinaryIO, str], List[Tuple[BinaryIO, str]]],
        storage_dir: str,
        entity_name: str,
        entity_ulid: str,
        db_session: AsyncSession
    ) -> List[Dict[str, Any]]:
        """파일(들)을 저장하고 메타데이터 반환
        
        Args:
            files: 단일 파일 튜플 (file, original_name) 또는 파일 튜플 리스트
            storage_dir (str): 저장 디렉토리 경로
            entity_name (str): 엔티티 이름
            entity_ulid (str): 엔티티 ULID
            db_session (AsyncSession): DB 세션
            
        Returns:
            List[Dict[str, Any]]: 저장된 파일들의 메타데이터 리스트
        """
        file_infos = []
        # 단일 파일인 경우 리스트로 변환
        files_list = [files] if isinstance(files, tuple) else files
        
        for file, original_name in files_list:
            # 파일 저장 및 메타데이터 생성
            file_info = await FileHandler._save_file(
                file=file,
                original_name=original_name,
                storage_dir=storage_dir,
                entity_name=entity_name,
                entity_ulid=entity_ulid
            )
            
            # DB에 파일 정보 저장 (트랜잭션은 BaseService에서 관리)
            result = await db_session.execute(
                text("""
                    INSERT INTO files (
                        entity_name, entity_ulid, original_name, storage_path,
                        mime_type, size, checksum
                    ) VALUES (
                        :entity_name, :entity_ulid, :original_name, :storage_path,
                        :mime_type, :size, :checksum
                    ) RETURNING *
                """),
                {
                    "entity_name": entity_name,
                    "entity_ulid": entity_ulid,
                    "original_name": file_info["original_name"],
                    "storage_path": file_info["storage_path"],
                    "mime_type": file_info["mime_type"],
                    "size": file_info["size"],
                    "checksum": file_info["checksum"]
                }
            )
            
            file_info = dict(result.fetchone())
            file_infos.append(file_info)
            
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