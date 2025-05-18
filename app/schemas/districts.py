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


# Base District Schema for shared properties
class DistrictBase(BaseModel):
    name: str
    code: str
    region_id: int


# Create schema for API request
class DistrictCreate(DistrictBase):
    pass


# District summary for list responses
class DistrictSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str


# paginated request for districts list
class PaginatedDistrictRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    search_term: Optional[str] = None
    sort_by: Optional[SortOption] = None


# Paginated response for districts list
class PaginatedDistrictsResponse(BaseModel):
    items: List[DistrictSummary]
    total_items: int
    total_pages: int
    current_page: int


# response for created district
class DistrictOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    region_id: int
