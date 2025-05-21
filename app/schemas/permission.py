from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from app.schemas.base import BaseSchema, TimestampMixin


class PermissionBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class Permission(PermissionBase, TimestampMixin, BaseSchema):
    id: int

    class Config:
        from_attributes = True
