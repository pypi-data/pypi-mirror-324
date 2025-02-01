from typing import Optional
from pydantic import BaseSchema, Field
from datetime import date

class BaseTaskSchema(BaseSchema):
    title: Optional[str] = None
    user_ulid: Optional[str] = None
    start_date: Optional[date] = Field(None, json_schema_extra={"format": "date", "allow_empty": True})
    end_date: Optional[date] = Field(None, json_schema_extra={"format": "date", "allow_empty": True})
    status: Optional[ProjectStatus] = None
    project_ulid: Optional[str] = None
    description: Optional[str] = None 