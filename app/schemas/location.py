from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema, DateMixin, TimestampMixin


class ContinentBase(BaseModel):
    name: str
    code: str
    name_code: Optional[str] = None
    background_image: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    status: int = 1


class ContinentCreate(ContinentBase):
    pass


class ContinentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    name_code: Optional[str] = None
    background_image: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    status: Optional[int] = None


class Continent(ContinentBase, DateMixin, BaseSchema):
    id: int


class ContinentWithCountries(Continent):
    countries: List["Country"] = []


class CountryBase(BaseModel):
    name: str
    code: str
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    background_image: Optional[str] = None
    logo: Optional[str] = None
    status: int = 1
    continent_id: int


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    background_image: Optional[str] = None
    logo: Optional[str] = None
    status: Optional[int] = None
    continent_id: Optional[int] = None


class Country(CountryBase, DateMixin, BaseSchema):
    id: int


class RegionBase(BaseModel):
    name: str
    code: str
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    background_image: Optional[str] = None
    logo: Optional[str] = None
    status: int = 1
    country_id: int


class RegionCreate(RegionBase):
    pass


class RegionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    background_image: Optional[str] = None
    logo: Optional[str] = None
    status: Optional[int] = None
    country_id: Optional[int] = None


class Region(RegionBase, DateMixin, BaseSchema):
    id: int


class DistrictBase(BaseModel):
    name: str
    code: str
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    background_image: Optional[str] = None
    logo: Optional[str] = None
    status: int = 1
    region_id: int


class DistrictCreate(DistrictBase):
    pass


class DistrictUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    background_image: Optional[str] = None
    logo: Optional[str] = None
    status: Optional[int] = None
    region_id: Optional[int] = None


class District(DistrictBase, DateMixin, BaseSchema):
    id: int


class WardBase(BaseModel):
    name: str
    code: str
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    background_image: Optional[str] = None
    logo: Optional[str] = None
    status: int = 1
    district_id: int


class WardCreate(WardBase):
    pass


class WardUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    background_image: Optional[str] = None
    logo: Optional[str] = None
    status: Optional[int] = None
    district_id: Optional[int] = None


class Ward(WardBase, DateMixin, BaseSchema):
    id: int


class LocationCategoryBase(BaseModel):
    name: str
    status: bool = True


class LocationCategoryCreate(LocationCategoryBase):
    pass


class LocationCategoryUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None


class LocationCategory(LocationCategoryBase, TimestampMixin, BaseSchema):
    id: int


class LocationBase(BaseModel):
    name: str
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geom: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    ward_id: Optional[int] = None
    category_id: int
    thumbnail_url: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    is_active: bool = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geom: Optional[str] = None
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


class Location(LocationBase, TimestampMixin, BaseSchema):
    id: int
    popularity_score: float = 0
    country: Optional[Country] = None
    region: Optional[Region] = None
    district: Optional[District] = None
    ward: Optional[Ward] = None
    category: Optional[LocationCategory] = None
