"""유효성 검사 관련 유틸리티 함수들을 모아둔 모듈입니다."""

from typing import Type, Dict, Any, Callable, TypeVar, Optional, List, Union
from functools import wraps
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from inspect import signature
from pydantic import BaseModel, field_validator
from datetime import datetime, date
import re

from .exceptions import ErrorCode, CustomException
from .base_model import Base

def validate_with(validator_func, unique_check=None, skip_if_none=False):
    """필드 유효성 검사 데코레이터
    Args:
        validator_func: 형식 검증 함수
        unique_check: (table_name, field) 튜플. 지정되면 해당 테이블의 필드에 대해 중복 검사 수행
        skip_if_none: None 값 허용 여부
    """
    def decorator(field_name: str):
        def validator(cls, value, info: Any):
            if skip_if_none and value is None:
                return value
            
            # 형식 검증 (필드명도 함께 전달)
            validator_func(value, field_name)
            
            # 중복 검사는 별도의 validator로 분리
            if unique_check:
                async def check_unique():
                    if not info or not hasattr(info, 'context'):
                        raise CustomException(
                            ErrorCode.VALIDATION_ERROR,
                            detail=f"{field_name}|{value}",
                            source_function=f"Validator.validate_{field_name}"
                        )
                    
                    db_service = info.context.get("db_service")
                    if not db_service:
                        raise CustomException(
                            ErrorCode.VALIDATION_ERROR,
                            detail=f"{field_name}|{value}",
                            source_function=f"Validator.validate_{field_name}"
                        )

                    table_name, field = unique_check
                    table = Base.metadata.tables.get(table_name)
                    if not table:
                        raise CustomException(
                            ErrorCode.VALIDATION_ERROR,
                            detail=f"{field_name}|{value}",
                            source_function=f"Validator.validate_{field_name}"
                        )

                    await db_service.validate_unique_fields(
                        table,
                        {field: value},
                        source_function=f"Validator.validate_{field_name}"
                    )
                
                # 중복 검사를 위한 별도의 validator 등록
                field_validator(field_name, mode='after')(check_unique)
            
            return value
        return field_validator(field_name, mode='before')(validator)
    return decorator

class Validator:
    @staticmethod
    def validate_email(email: str, field_name: str = "email") -> None:
        """이메일 형식 검증을 수행하는 메서드."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise CustomException(
                ErrorCode.FIELD_INVALID_EMAIL,
                detail=f"{field_name}|{email}",
                source_function="Validator.validate_email"
            )

    @staticmethod
    def validate_password(password: str, field_name: str = "password") -> None:
        """비밀번호 규칙 검증을 수행하는 메서드."""
        try:
            if len(password) < 8:
                raise CustomException(
                    ErrorCode.FIELD_INVALID_PASSWORD_LENGTH,
                    detail=f"{field_name}|{password}",
                    source_function="Validator.validate_password"
                )
            
            if not re.search(r'[A-Z]', password):
                raise CustomException(
                    ErrorCode.FIELD_INVALID_PASSWORD_UPPER,
                    detail=f"{field_name}|{password}",
                    source_function="Validator.validate_password"
                )
            
            if not re.search(r'[0-9]', password):
                raise CustomException(
                    ErrorCode.FIELD_INVALID_PASSWORD_NUMBER,
                    detail=f"{field_name}|{password}",
                    source_function="Validator.validate_password"
                )
            
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise CustomException(
                    ErrorCode.FIELD_INVALID_PASSWORD_SPECIAL,
                    detail=f"{field_name}|{password}",
                    source_function="Validator.validate_password"
                )
            
        except CustomException as ce:
            raise ce
        except Exception as e:
            raise CustomException(
                ErrorCode.VALIDATION_ERROR,
                detail=f"{field_name}|{password}",
                source_function="Validator.validate_password"
            )

    @staticmethod
    def validate_id(value: str, field_name: str) -> None:
        """ID 형식 검증을 수행하는 메서드."""
        if len(value) < 3:
            raise CustomException(
                ErrorCode.FIELD_INVALID_ID_LENGTH,
                detail=f"{field_name}|{value}",
                source_function="Validator.validate_id"
            )
        if not re.match(r'^[a-z0-9_]+$', value):
            raise CustomException(
                ErrorCode.FIELD_INVALID_ID_CHARS,
                detail=f"{field_name}|{value}",
                source_function="Validator.validate_id"
            )

    @staticmethod
    def validate_mobile(mobile: str, field_name: str = "mobile") -> None:
        """휴대전화 번호 형식 검증을 수행하는 메서드."""
        if not mobile:  # Optional 필드이므로 빈 값 허용
            return
        
        pattern = r'^010-?[0-9]{4}-?[0-9]{4}$'
        if not re.match(pattern, mobile):
            raise CustomException(
                ErrorCode.INVALID_MOBILE,
                detail=f"{field_name}|{mobile}",
                source_function="Validator.validate_mobile"
            )

    @staticmethod
    def validate_phone(phone: str, field_name: str = "phone") -> None:
        """일반 전화번호 형식 검증을 수행하는 메서드."""
        if not phone:  # Optional 필드이므로 빈 값 허용
            return
        
        pattern = r'^(0[2-6][1-5]?)-?([0-9]{3,4})-?([0-9]{4})$'
        if not re.match(pattern, phone):
            raise CustomException(
                ErrorCode.FIELD_INVALID_PHONE,
                detail=f"{field_name}|{phone}",
                source_function="Validator.validate_phone"
            )

    @staticmethod
    def validate_name(name: str, field_name: str = "name") -> None:
        """이름 형식 검증을 수행하는 메서드."""
        if not name:
            raise CustomException(
                ErrorCode.VALIDATION_ERROR,
                detail=f"{field_name}|{name}",
                source_function="Validator.validate_name"
            )
        
        if len(name) < 2 or len(name) > 100:
            raise CustomException(
                ErrorCode.VALIDATION_ERROR,
                detail=f"{field_name}|{name}",
                source_function="Validator.validate_name"
            )
        
        # 한글, 영문, 공백만 허용
        if not re.match(r'^[가-힣a-zA-Z\s]+$', name):
            raise CustomException(
                ErrorCode.VALIDATION_ERROR,
                detail=f"{field_name}|{name}",
                source_function="Validator.validate_name"
            )

    @staticmethod
    def validate_date(value: Any, field_name: str = "date") -> Optional[date]:
        """날짜 형식 검증을 수행하는 메서드."""
        # 빈 값 처리를 가장 먼저
        if not value or str(value).strip() == "":
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        try:
            return datetime.strptime(str(value), '%Y-%m-%d').date()
        except Exception as e:
            raise CustomException(
                error_code=ErrorCode.VALIDATION_ERROR,
                detail=f"{field_name}|{value}",
                source_function="Validator.validate_date",
                original_error=str(e)
            )

    @staticmethod
    def validate_datetime(value: Any, field_name: str = "datetime") -> Optional[datetime]:
        """날짜+시간 형식 검증을 수행하는 메서드."""
        # 빈 값 처리를 가장 먼저
        if not value or str(value).strip() == "":
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        try:
            # ISO 형식 (YYYY-MM-DDTHH:MM:SS) 먼저 시도
            try:
                return datetime.fromisoformat(str(value))
            except:
                # 일반 날짜+시간 형식 시도
                return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            raise CustomException(
                error_code=ErrorCode.INVALID_DATETIME_FORMAT,
                detail=f"{field_name}|{value}",
                source_function="Validator.validate_datetime",
                original_error=str(e)
            )

def _create_validator(field_names: tuple[str, ...], 
                     validate_func: Callable,
                     field_type: Type,
                     error_code: ErrorCode,
                     source_prefix: str):
    """공통 validator 생성 함수
    Args:
        field_names: 검증할 필드명들
        validate_func: 실제 검증을 수행할 함수
        field_type: 필드 타입 (date 또는 datetime)
        error_code: 에러 발생시 사용할 에러 코드
        source_prefix: 에러 발생시 사용할 source_function 접두사
    """
    def decorator(cls):
        for field_name in field_names:
            field = cls.model_fields.get(field_name)
            if field:
                field.annotation = Optional[field_type]
                field.default = None
                
            @field_validator(field_name, mode='before')
            @classmethod
            def validate(cls, value: Any, info: Any) -> Any:
                # 빈 값 처리를 가장 먼저, 더 엄격하게
                if not value or str(value).strip() == "":
                    return None
                try:
                    return validate_func(value, field_name)
                except CustomException as e:
                    raise e
                except Exception as e:
                    raise CustomException(
                        error_code=error_code,
                        detail=f"{field_name}|{value}",
                        source_function=f"{source_prefix}.{field_name}",
                        original_error=str(e)
                    )
            setattr(cls, f'validate_{field_name}', validate)
        return cls
    return decorator

def date_validator(*field_names: str):
    """날짜 필드 유효성 검사 데코레이터"""
    return _create_validator(
        field_names=field_names,
        validate_func=Validator.validate_date,
        field_type=date,
        error_code=ErrorCode.VALIDATION_ERROR,
        source_prefix="date_validator"
    )

def datetime_validator(*field_names: str):
    """날짜+시간 필드 유효성 검사 데코레이터"""
    return _create_validator(
        field_names=field_names,
        validate_func=Validator.validate_datetime,
        field_type=datetime,
        error_code=ErrorCode.VALIDATION_ERROR,
        source_prefix="datetime_validator"
    )
