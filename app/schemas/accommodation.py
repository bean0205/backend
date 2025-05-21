from datetime import time
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.base import BaseSchema, TimestampMixin


class AccommodationCategoryBase(BaseModel):
    name: str
    status: bool = True


class AccommodationCategoryCreate(AccommodationCategoryBase):
    pass


class AccommodationCategoryUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None


class AccommodationCategory(AccommodationCategoryBase, TimestampMixin, BaseSchema):
    id: int


class AccommodationBase(BaseModel):
    user_id: int
    name: str
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geom: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    ward_id: Optional[int] = None
    category_id: int
    thumbnail_url: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    checkin_time: Optional[time] = None
    checkout_time: Optional[time] = None
    cancel_policy: Optional[str] = None
    pet_policy: Optional[str] = None
    child_policy: Optional[str] = None
    is_active: bool = True


class AccommodationCreate(AccommodationBase):
    pass


class AccommodationUpdate(BaseModel):
    name: Optional[str] = None
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geom: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    ward_id: Optional[int] = None
    category_id: Optional[int] = None
    thumbnail_url: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    checkin_time: Optional[time] = None
    checkout_time: Optional[time] = None
    cancel_policy: Optional[str] = None
    pet_policy: Optional[str] = None
    child_policy: Optional[str] = None
    is_active: Optional[bool] = None
    popularity_score: Optional[float] = None


class Accommodation(AccommodationBase, TimestampMixin, BaseSchema):
    id: int
    popularity_score: float = 0


class AccommodationRoomBase(BaseModel):
    accommodation_id: int
    name: str
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    adult_capacity: int = 1
    child_capacity: int = 0
    room_area: Optional[int] = None
    bed_capacity: Optional[str] = None
    status: int = 1


class AccommodationRoomCreate(AccommodationRoomBase):
    pass


class AccommodationRoomUpdate(BaseModel):
    name: Optional[str] = None
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    adult_capacity: Optional[int] = None
    child_capacity: Optional[int] = None
    room_area: Optional[int] = None
    bed_capacity: Optional[str] = None
    status: Optional[int] = None


class AccommodationRoom(AccommodationRoomBase, TimestampMixin, BaseSchema):
    id: int
