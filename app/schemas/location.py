from datetime import datetime
from typing import Optional, List, Any, Dict
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


# Location amenity schema
class LocationAmenityCreate(BaseModel):
    name: str


# Location amenity response
class LocationAmenityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


# Base Location Schema for shared properties
class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None
    latitude: float
    longitude: float
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
    popularity_score: float = 0.0
    is_active: bool = True


# Create schema for API request
class LocationCreate(LocationBase):
    amenities: Optional[List[str]] = None


# Update schema for API request
class LocationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
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
    popularity_score: Optional[float] = None
    is_active: Optional[bool] = None
    amenities: Optional[List[str]] = None


# Schema for API responses
class LocationOut(LocationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    address_short: str
    average_rating: Optional[float] = None
    amenities: List[LocationAmenityOut] = []
    created_at: datetime
    updated_at: datetime


# Filter and pagination parameters
class LocationFilterParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    search_term: Optional[str] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    ward_id: Optional[int] = None
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
    price_min: Optional[float] = None
    price_max: Optional[float] = None


# Paginated response for location list
class PaginatedLocationResponse(BaseModel):
    items: List[LocationSummary]
    total_items: int
    total_pages: int
    current_page: int


# Used for location search by coordinates
class NearbyLocationRequest(BaseModel):
    latitude: float = Field(..., description="Latitude of the center point")
    longitude: float = Field(..., description="Longitude of the center point")
    radius: float = Field(default=5.0, description="Search radius in kilometers", ge=0.1, le=50.0)
    limit: int = Field(default=20, description="Maximum number of results to return", ge=1, le=100)
    category_id: Optional[int] = None
