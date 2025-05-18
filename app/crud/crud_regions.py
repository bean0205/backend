from typing import List, Optional, Union, Dict, Any, Tuple

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc, and_, or_, Float

from app.db.models import Location, Category, Country, Region, LocationAmenity, LocationAmenity, Rating
from app.schemas.regions import RegionCreate, PaginatedCountriesResponse, SortOption, PaginatedRegionRequest


class CRUDRegions:
    async def get_by_code(self, db: AsyncSession, code: str) -> Optional[Region]:
        """
        Get a region by its code.
        """
        result = await db.execute(
            select(Region).where(Region.code == code)
        )
        return result.scalars().first()

    async def create(self, db: AsyncSession, obj_in: RegionCreate) -> Region:
        """
        Create a new region.
        """
        db_region = Region(**obj_in.dict())
        db.add(db_region)
        await db.commit()
        await db.refresh(db_region)
        return db_region

    async def update(self, db: AsyncSession, id: int, obj_in: RegionCreate) -> Region:
        """
        Update an existing region.
        """
        region = await self.get_by_id(db, id)
        if not region:
            raise HTTPException(status_code=404, detail="Region not found")
        for key, value in obj_in.dict().items():
            setattr(region, key, value)
        await db.commit()
        await db.refresh(region)
        return region

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[Region]:
        """
        Get a region by its ID.
        """
        result = await db.execute(
            select(Region).where(Region.id == id)
        )
        return result.scalars().first()

    async def delete(self, db: AsyncSession, id: int) -> None:
        """
        Delete a region by its ID.
        """
        region = await self.get_by_id(db, id)
        if not region:
            raise HTTPException(status_code=404, detail="Region not found")
        await db.delete(region)
        await db.commit()

    async def get_paginated_regions(self, db: AsyncSession,
                                    params: PaginatedRegionRequest) -> PaginatedCountriesResponse:
        """
        Get a paginated list of regions.
        """
        query = select(Region)
        if params.search_term:
            query = query.where(
                or_(
                    Region.name.ilike(f"%{params.search_term}%"),
                    Region.code.ilike(f"%{params.search_term}%")
                )
            )

        if params.sort_by == SortOption.CODE_DESC:
            query = query.order_by(desc(Region.code))
        elif params.sort_by == SortOption.CODE_ASC:
            query = query.order_by(asc(Region.code))
        elif params.sort_by == SortOption.NAME_ASC:
            query = query.order_by(asc(Region.name))
        elif params.sort_by == SortOption.NAME_DESC:
            query = query.order_by(desc(Region.name))

        total_items = await db.execute(select(func.count()).select_from(query.subquery()))
        total_items = total_items.scalar()

        # Apply pagination
        offset = (params.page - 1) * params.size
        query = query.offset(offset).limit(params.size)

        result = await db.execute(query)
        items = result.scalars().all()

        return PaginatedCountriesResponse(
            items=items,
            total_items=total_items,
            total_pages=(total_items // params.size) + (1 if total_items % params.size > 0 else 0),
            current_page=params.page
        )


regions = CRUDRegions()
