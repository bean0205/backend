from typing import List, Optional, Dict, Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models import FoodCategory, Food, Rating
from app.schemas.food import (
    FoodCategoryCreate, FoodCategoryUpdate,
    FoodCreate, FoodUpdate,
    RatingCreate, RatingUpdate
)
from app.schemas.base import PaginationParams


class CRUDFoodCategory(CRUDBase[FoodCategory, FoodCategoryCreate, FoodCategoryUpdate]):
    async def get_all_active(self, db: AsyncSession) -> List[FoodCategory]:
        """Get all active food categories"""
        result = await db.execute(
            select(FoodCategory).filter(FoodCategory.status == True)
        )
        return result.scalars().all()


class CRUDFood(CRUDBase[Food, FoodCreate, FoodUpdate]):
    async def get_by_category(
            self, db: AsyncSession, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Food]:
        """Get foods by category ID"""
        result = await db.execute(
            select(Food)
            .filter(Food.category_id == category_id)
            .filter(Food.status == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_location(
            self,
            db: AsyncSession,
            *,
            country_id: Optional[int] = None,
            region_id: Optional[int] = None,
            district_id: Optional[int] = None,
            ward_id: Optional[int] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[Food]:
        """Get foods by location"""
        query = select(Food).filter(Food.status == True)

        if country_id:
            query = query.filter(Food.country_id == country_id)

        if region_id:
            query = query.filter(Food.region_id == region_id)

        if district_id:
            query = query.filter(Food.district_id == district_id)

        if ward_id:
            query = query.filter(Food.ward_id == ward_id)

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def search_foods(
            self,
            db: AsyncSession,
            *,
            search_term: Optional[str] = None,
            category_id: Optional[int] = None,
            country_id: Optional[int] = None,
            region_id: Optional[int] = None,
            district_id: Optional[int] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None,
            params: PaginationParams
    ) -> Dict[str, Any]:
        """Search foods with various filters and pagination"""
        # Main query for items
        query = select(Food).filter(Food.status == True)

        # Apply filters
        if search_term:
            query = query.filter(Food.name.ilike(f"%{search_term}%"))

        if category_id:
            query = query.filter(Food.category_id == category_id)

        if country_id:
            query = query.filter(Food.country_id == country_id)

        if region_id:
            query = query.filter(Food.region_id == region_id)

        if district_id:
            query = query.filter(Food.district_id == district_id)

        if min_price is not None:
            query = query.filter(Food.price_min >= min_price)

        if max_price is not None:
            query = query.filter(Food.price_min <= max_price)

        # Count query
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0

        # Apply pagination
        offset = (params.page - 1) * params.limit
        query = query.offset(offset).limit(params.limit)

        # Get paginated results
        result = await db.execute(query)
        items = result.scalars().all()

        # Calculate total pages
        total_pages = (total + params.limit - 1) // params.limit if total > 0 else 0

        return {
            "items": items,
            "total": total,
            "page": params.page,
            "limit": params.limit,
            "pages": total_pages
        }


class CRUDRating(CRUDBase[Rating, RatingCreate, RatingUpdate]):
    async def get_by_reference(
            self,
            db: AsyncSession,
            *,
            reference_id: int,
            reference_type: str,
            skip: int = 0,
            limit: int = 100
    ) -> List[Rating]:
        """Get ratings by reference ID and type"""
        result = await db.execute(
            select(Rating)
            .filter(Rating.reference_id == reference_id)
            .filter(Rating.reference_type == reference_type)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_user_rating(
            self,
            db: AsyncSession,
            *,
            user_id: int,
            reference_id: int,
            reference_type: str
    ) -> Optional[Rating]:
        """Get a user's rating for a specific item"""
        result = await db.execute(
            select(Rating)
            .filter(Rating.user_id == user_id)
            .filter(Rating.reference_id == reference_id)
            .filter(Rating.reference_type == reference_type)
        )
        return result.scalars().first()

    async def get_average_rating(
            self,
            db: AsyncSession,
            *,
            reference_id: int,
            reference_type: str
    ) -> float:
        """Calculate average rating for a reference"""
        result = await db.execute(
            select(func.avg(Rating.rating))
            .filter(Rating.reference_id == reference_id)
            .filter(Rating.reference_type == reference_type)
        )
        return result.scalar() or 0.0


food_category = CRUDFoodCategory(FoodCategory)
food = CRUDFood(Food)
rating = CRUDRating(Rating)
