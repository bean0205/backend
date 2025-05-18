from typing import List, Optional, Union, Dict, Any, Tuple

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc, and_, or_, Float

from app.db.models import District
from app.schemas.districts import DistrictCreate, PaginatedDistrictsResponse, SortOption, PaginatedDistrictRequest


class CRUDDistricts:
    async def get_by_code(self, db: AsyncSession, code: str) -> Optional[District]:
        """
        Get a district by its code.
        """
        result = await db.execute(
            select(District).where(District.code == code)
        )
        return result.scalars().first()

    async def create(self, db: AsyncSession, obj_in: DistrictCreate) -> District:
        """
        Create a new district.
        """
        db_district = District(**obj_in.dict())
        db.add(db_district)
        await db.commit()
        await db.refresh(db_district)
        return db_district

    async def update(self, db: AsyncSession, id: int, obj_in: DistrictCreate) -> District:
        """
        Update an existing district.
        """
        district = await self.get_by_id(db, id)
        if not district:
            raise HTTPException(status_code=404, detail="District not found")
        for key, value in obj_in.dict().items():
            setattr(district, key, value)
        await db.commit()
        await db.refresh(district)
        return district

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[District]:
        """
        Get a district by its ID.
        """
        result = await db.execute(
            select(District).where(District.id == id)
        )
        return result.scalars().first()

    async def delete(self, db: AsyncSession, id: int) -> None:
        """
        Delete a district by its ID.
        """
        district = await self.get_by_id(db, id)
        if not district:
            raise HTTPException(status_code=404, detail="District not found")
        await db.delete(district)
        await db.commit()

    async def get_by_region_id(self, db: AsyncSession, region_id: int) -> List[District]:
        """
        Get all districts for a specific region.
        """
        result = await db.execute(
            select(District).where(District.region_id == region_id)
        )
        return result.scalars().all()

    async def get_paginated_districts(self, db: AsyncSession,
                                      params: PaginatedDistrictRequest) -> PaginatedDistrictsResponse:
        """
        Get a paginated list of districts.
        """
        query = select(District)
        if params.search_term:
            query = query.where(
                or_(
                    District.name.ilike(f"%{params.search_term}%"),
                    District.code.ilike(f"%{params.search_term}%")
                )
            )

        if params.sort_by == SortOption.CODE_DESC:
            query = query.order_by(desc(District.code))
        elif params.sort_by == SortOption.CODE_ASC:
            query = query.order_by(asc(District.code))
        elif params.sort_by == SortOption.NAME_ASC:
            query = query.order_by(asc(District.name))
        elif params.sort_by == SortOption.NAME_DESC:
            query = query.order_by(desc(District.name))

        total_items = await db.execute(select(func.count()).select_from(query.subquery()))
        total_items = total_items.scalar()

        # Apply pagination
        offset = (params.page - 1) * params.size
        query = query.offset(offset).limit(params.size)

        result = await db.execute(query)
        items = result.scalars().all()

        return PaginatedDistrictsResponse(
            items=items,
            total_items=total_items,
            total_pages=(total_items // params.size) + (1 if total_items % params.size > 0 else 0),
            current_page=params.page
        )


districts = CRUDDistricts()
