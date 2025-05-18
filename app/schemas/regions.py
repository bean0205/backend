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


# Base Location Schema for shared properties
class RegionBase(BaseModel):
    name: str
    code: str
    country_id: int


# Create schema for API request
class RegionCreate(RegionBase):
    pass


# Location summary for list responses
class LocationSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str


# paginated request for countries list
class PaginatedRegionRequest(BaseModel):
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
class RegionOut(BaseModel):
    id: int
    name: str
    country_id: int

    class Config:
        orm_mode = True
