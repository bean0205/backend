from datetime import datetime
from typing import Optional, List, Literal
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, field_validator


# Sorting options enum
class SortOption(str, Enum):
    POPULARITY_DESC = "popularity_desc"
    POPULARITY_ASC = "popularity_asc"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"
    RATING_DESC = "rating_desc"
    RATING_ASC = "rating_asc"
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"


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


# Filter and pagination parameters
class LocationFilterParams(BaseModel):
    page: int = 1
    size: int = 20
    search_term: Optional[str] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    category_id: Optional[int] = None
    price_range_min: Optional[float] = None
    price_range_max: Optional[float] = None
    amenities: Optional[List[str]] = None
    min_rating: Optional[float] = None
    sort_by: Optional[SortOption] = None
    
    @field_validator('page')
    def validate_page(cls, v):
        if v < 1:
            return 1
        return v
    
    @field_validator('size')
    def validate_size(cls, v):
        if v < 1:
            return 20
        if v > 100:
            return 100
        return v


# Location summary for list responses
class LocationSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    thumbnail_url: Optional[str] = None
    address_short: str
    category_name: Optional[str] = None
    average_rating: Optional[float] = None


# Paginated response for location list
class PaginatedLocationResponse(BaseModel):
    items: List[LocationSummary]
    total_items: int
    total_pages: int
    current_page: int


class LocationList(BaseModel):
    items: List[Location]
    total: int
