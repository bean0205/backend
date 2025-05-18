from datetime import datetime
from typing import Optional, List, Literal
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, field_validator


# Sorting options enum
class SortOption(str, Enum):
    CODE_DESC = "code_desc"
    CODE_ASC = "code_asc"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"


# Base Country Schema for shared properties
class CountryBase(BaseModel):
    code: str
    name: str
    continent_id: int


# Create schema for API request
class CountryCreate(CountryBase):
    pass


# Update schema for API request
class CountryUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    continent_id: Optional[int] = None


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


# Country summary for list responses
class CountrySummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str


# paginated request for countries list
class PaginatedCountriesRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    search_term: Optional[str] = None
    continent_id: Optional[int] = None
    sort_by: Optional[SortOption] = None


# Paginated response for countries list
class PaginatedCountriesResponse(BaseModel):
    items: List[CountrySummary]
    total_items: int
    total_pages: int
    current_page: int


# response for country
class CountryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    continent_id: int
