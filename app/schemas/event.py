from datetime import date, time
from typing import List, Optional
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.base import BaseSchema, TimestampMixin


class OrganizerBase(BaseModel):
    user_id: int
    name: str
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    status: bool = True


class OrganizerCreate(OrganizerBase):
    pass


class OrganizerUpdate(BaseModel):
    name: Optional[str] = None
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    status: Optional[bool] = None


class Organizer(OrganizerBase, TimestampMixin, BaseSchema):
    id: int


class EventCategoryBase(BaseModel):
    name: str
    status: bool = True


class EventCategoryCreate(EventCategoryBase):
    pass


class EventCategoryUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None


class EventCategory(EventCategoryBase, TimestampMixin, BaseSchema):
    id: int


class EventBase(BaseModel):
    user_id: int
    organizer_id: int
    category_id: int
    name: str
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    content: Optional[str] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    ward_id: Optional[int] = None
    thumbnail_url: Optional[str] = None
    start_time: Optional[time] = None
    start_date: date
    end_date: Optional[date] = None
    price: Optional[Decimal] = None
    max_attendees: Optional[int] = None
    status: bool = True


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    organizer_id: Optional[int] = None
    category_id: Optional[int] = None
    name: Optional[str] = None
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    content: Optional[str] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    ward_id: Optional[int] = None
    thumbnail_url: Optional[str] = None
    start_time: Optional[time] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    price: Optional[Decimal] = None
    max_attendees: Optional[int] = None
    view_count: Optional[int] = None
    status: Optional[bool] = None


class Event(EventBase, TimestampMixin, BaseSchema):
    id: int
    view_count: int = 0


class EventAttendeeBase(BaseModel):
    user_id: int
    event_id: int
    status: bool = True


class EventAttendeeCreate(EventAttendeeBase):
    pass


class EventAttendeeUpdate(BaseModel):
    status: Optional[bool] = None


class EventAttendee(EventAttendeeBase, TimestampMixin, BaseSchema):
    id: int


class EventSponsorBase(BaseModel):
    organizer_id: int
    event_id: int
    status: bool = True


class EventSponsorCreate(EventSponsorBase):
    pass


class EventSponsorUpdate(BaseModel):
    status: Optional[bool] = None


class EventSponsor(EventSponsorBase, TimestampMixin, BaseSchema):
    id: int
