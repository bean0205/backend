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


# Base Ward Schema for shared properties
class WardBase(BaseModel):
    name: str
    code: str
    district_id: int


# Create schema for API request
class WardCreate(WardBase):
    pass


# Ward summary for list responses
class WardSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str


# paginated request for wards list
class PaginatedWardRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    search_term: Optional[str] = None
    sort_by: Optional[SortOption] = None


# Paginated response for wards list
class PaginatedWardsResponse(BaseModel):
    items: List[WardSummary]
    total_items: int
    total_pages: int
    current_page: int


# response for created ward
class WardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    district_id: int
