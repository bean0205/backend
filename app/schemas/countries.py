from datetime import datetime
from typing import Optional, List, Literal
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, field_validator


# Sorting options enum
class SortOption(str, Enum):
    CODE_DESC = "popularity_desc"
    CODE_ASC = "popularity_asc"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"


# Base Location Schema for shared properties
class CountryBase(BaseModel):
    code: str
    name: str


# Create schema for API request
class CountryCreate(CountryBase):
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
    code: str
    name: str


# paginated request for countries list
class PaginatedCountriesRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    search_term: Optional[str] = None
    sort_by: Optional[SortOption] = None

# Paginated response for countries list
class PaginatedCountriesResponse(BaseModel):
    items: List[LocationSummary]
    total_items: int
    total_pages: int
    current_page: int


# response for created contruy
class CountryOut(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        orm_mode = True
