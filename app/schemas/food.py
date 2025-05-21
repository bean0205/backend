from typing import List, Optional

from pydantic import BaseModel

from app.schemas.base import BaseSchema, TimestampMixin


class FoodCategoryBase(BaseModel):
    name: str
    status: bool = True


class FoodCategoryCreate(FoodCategoryBase):
    pass


class FoodCategoryUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None


class FoodCategory(FoodCategoryBase, TimestampMixin, BaseSchema):
    id: int


class FoodBase(BaseModel):
    name: str
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    ward_id: Optional[int] = None
    category_id: int
    thumbnail_url: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    status: bool = True


class FoodCreate(FoodBase):
    pass


class FoodUpdate(BaseModel):
    name: Optional[str] = None
    name_code: Optional[str] = None
    description: Optional[str] = None
    description_code: Optional[str] = None
    country_id: Optional[int] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    ward_id: Optional[int] = None
    category_id: Optional[int] = None
    thumbnail_url: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    popularity_score: Optional[float] = None
    status: Optional[bool] = None


class Food(FoodBase, TimestampMixin, BaseSchema):
    id: int
    popularity_score: float = 0


class RatingBase(BaseModel):
    reference_id: int
    reference_type: str
    user_id: int
    rating: float
    comment: Optional[str] = None


class RatingCreate(RatingBase):
    pass


class RatingUpdate(BaseModel):
    rating: Optional[float] = None
    comment: Optional[str] = None


class Rating(RatingBase, TimestampMixin, BaseSchema):
    id: int
