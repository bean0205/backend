from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from app.schemas.base import BaseSchema, TimestampMixin
from app.schemas.permission import Permission


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_default: bool = False


class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    permission_ids: Optional[List[int]] = None


class Role(RoleBase, TimestampMixin, BaseSchema):
    id: int
    permissions: Optional[List[Permission]] = []

    class Config:
        from_attributes = True
