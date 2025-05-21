from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.base import BaseSchema, DateMixin, TimestampMixin


class MediaTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: int = 1


class MediaTypeCreate(MediaTypeBase):
    pass


class MediaTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None


class MediaType(MediaTypeBase, DateMixin, BaseSchema):
    id: int


class MediaCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: int = 1


class MediaCategoryCreate(MediaCategoryBase):
    pass


class MediaCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None


class MediaCategory(MediaCategoryBase, DateMixin, BaseSchema):
    id: int


class MediaBase(BaseModel):
    type_id: int
    category_id: int
    reference_id: int
    reference_type: str
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    status: int = 1


class MediaCreate(MediaBase):
    pass


class MediaUpdate(BaseModel):
    type_id: Optional[int] = None
    category_id: Optional[int] = None
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None


class Media(MediaBase, DateMixin, BaseSchema):
    id: int
