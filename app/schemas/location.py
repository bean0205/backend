from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


# Base Location Schema for shared properties
class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    is_active: bool = True


# Create schema for API request
class LocationCreate(LocationBase):
    pass


# Update schema for API request
class LocationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None


# Schema for API responses
class Location(LocationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime


class LocationList(BaseModel):
    items: List[Location]
    total: int
