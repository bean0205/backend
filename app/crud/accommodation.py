from typing import List, Optional, Dict, Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models import AccommodationCategory, Accommodation, AccommodationRoom
from app.schemas.accommodation import (
    AccommodationCategoryCreate, AccommodationCategoryUpdate,
    AccommodationCreate, AccommodationUpdate,
    AccommodationRoomCreate, AccommodationRoomUpdate
)
from app.schemas.base import PaginationParams


class CRUDAccommodationCategory(
    CRUDBase[AccommodationCategory, AccommodationCategoryCreate, AccommodationCategoryUpdate]):
    async def get_all_active(self, db: AsyncSession) -> List[AccommodationCategory]:
        """Get all active accommodation categories"""
        result = await db.execute(
            select(AccommodationCategory).filter(AccommodationCategory.status == True)
        )
        return result.scalars().all()


class CRUDAccommodation(CRUDBase[Accommodation, AccommodationCreate, AccommodationUpdate]):
    async def get_by_user(
            self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Accommodation]:
        """Get accommodations by user ID"""
        result = await db.execute(
            select(Accommodation)
            .filter(Accommodation.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_category(
            self, db: AsyncSession, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Accommodation]:
        """Get accommodations by category ID"""
        result = await db.execute(
            select(Accommodation)
            .filter(Accommodation.category_id == category_id)
            .filter(Accommodation.is_active == True)
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
    ) -> List[Accommodation]:
        """Get accommodations by location"""
        query = select(Accommodation).filter(Accommodation.is_active == True)

        if country_id:
            query = query.filter(Accommodation.country_id == country_id)

        if region_id:
            query = query.filter(Accommodation.region_id == region_id)

        if district_id:
            query = query.filter(Accommodation.district_id == district_id)

        if ward_id:
            query = query.filter(Accommodation.ward_id == ward_id)

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def search_accommodations(
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
        """Search accommodations with various filters"""
        # Main query for items
        query = select(Accommodation).filter(Accommodation.is_active == True)

        # Apply filters
        if search_term:
            query = query.filter(Accommodation.name.ilike(f"%{search_term}%"))

        if category_id:
            query = query.filter(Accommodation.category_id == category_id)

        if country_id:
            query = query.filter(Accommodation.country_id == country_id)

        if region_id:
            query = query.filter(Accommodation.region_id == region_id)

        if district_id:
            query = query.filter(Accommodation.district_id == district_id)

        if min_price is not None:
            query = query.filter(Accommodation.price_min >= min_price)

        if max_price is not None:
            query = query.filter(Accommodation.price_min <= max_price)

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


class CRUDAccommodationRoom(CRUDBase[AccommodationRoom, AccommodationRoomCreate, AccommodationRoomUpdate]):
    async def get_by_accommodation(
            self, db: AsyncSession, *, accommodation_id: int, skip: int = 0, limit: int = 100
    ) -> List[AccommodationRoom]:
        """Get rooms by accommodation ID"""
        result = await db.execute(
            select(AccommodationRoom)
            .filter(AccommodationRoom.accommodation_id == accommodation_id)
            .filter(AccommodationRoom.status == 1)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


accommodation_category = CRUDAccommodationCategory(AccommodationCategory)
accommodation = CRUDAccommodation(Accommodation)
accommodation_room = CRUDAccommodationRoom(AccommodationRoom)
