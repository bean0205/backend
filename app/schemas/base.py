from datetime import datetime, date, time
from typing import List, Optional
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2


class TimestampMixin(BaseModel):
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class DateMixin(BaseModel):
    created_date: date = None
    updated_date: Optional[date] = None


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)


class PaginatedResponse(BaseModel):
    items: List = []
    total: int
    page: int
    limit: int
    pages: int
