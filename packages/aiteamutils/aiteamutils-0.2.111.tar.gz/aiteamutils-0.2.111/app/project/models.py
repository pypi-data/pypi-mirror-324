from sqlalchemy import String, Date, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from datetime import datetime, date
from pydantic import Field

from aiteamutils.base_model import BaseColumn, BaseSchema
from aiteamutils.exceptions import CustomException, ErrorCode
from aiteamutils.validators import date_validator
from app.utils.enums import ProjectStatus

if TYPE_CHECKING:
    from app.task.models import Task

@date_validator('start_date', 'end_date')
class BaseProjectSchema(BaseSchema):
    title: Optional[str] = None
    user_ulid: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[ProjectStatus] = None 