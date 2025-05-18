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


# Base Continent Schema for shared properties
class ContinentBase(BaseModel):
    code: str
    name: str


# Create schema for API request
class ContinentCreate(ContinentBase):
    pass


# Update schema for API request
class ContinentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None


# Continent summary for list responses
class ContinentSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str


# paginated request for continents list
class PaginatedContinentsRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    search_term: Optional[str] = None
    sort_by: Optional[SortOption] = None


# Paginated response for continents list
class PaginatedContinentsResponse(BaseModel):
    items: List[ContinentSummary]
    total_items: int
    total_pages: int
    current_page: int


# response for continent
class ContinentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
