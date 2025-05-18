from typing import List, Optional, Union, Dict, Any, Tuple

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc, and_, or_, Float

from app.db.models import Ward
from app.schemas.wards import WardCreate, PaginatedWardsResponse, SortOption, PaginatedWardRequest


class CRUDWards:
    async def get_by_code(self, db: AsyncSession, code: str) -> Optional[Ward]:
        """
        Get a ward by its code.
        """
        result = await db.execute(
            select(Ward).where(Ward.code == code)
        )
        return result.scalars().first()

    async def create(self, db: AsyncSession, obj_in: WardCreate) -> Ward:
        """
        Create a new ward.
        """
        db_ward = Ward(**obj_in.dict())
        db.add(db_ward)
        await db.commit()
        await db.refresh(db_ward)
        return db_ward

    async def update(self, db: AsyncSession, id: int, obj_in: WardCreate) -> Ward:
        """
        Update an existing ward.
        """
        ward = await self.get_by_id(db, id)
        if not ward:
            raise HTTPException(status_code=404, detail="Ward not found")
        for key, value in obj_in.dict().items():
            setattr(ward, key, value)
        await db.commit()
        await db.refresh(ward)
        return ward

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[Ward]:
        """
        Get a ward by its ID.
        """
        result = await db.execute(
            select(Ward).where(Ward.id == id)
        )
        return result.scalars().first()

    async def delete(self, db: AsyncSession, id: int) -> None:
        """
        Delete a ward by its ID.
        """
        ward = await self.get_by_id(db, id)
        if not ward:
            raise HTTPException(status_code=404, detail="Ward not found")
        await db.delete(ward)
        await db.commit()

    async def get_by_district_id(self, db: AsyncSession, district_id: int) -> List[Ward]:
        """
        Get all wards for a specific district.
        """
        result = await db.execute(
            select(Ward).where(Ward.district_id == district_id)
        )
        return result.scalars().all()

    async def get_paginated_wards(self, db: AsyncSession,
                                  params: PaginatedWardRequest) -> PaginatedWardsResponse:
        """
        Get a paginated list of wards.
        """
        query = select(Ward)
        if params.search_term:
            query = query.where(
                or_(
                    Ward.name.ilike(f"%{params.search_term}%"),
                    Ward.code.ilike(f"%{params.search_term}%")
                )
            )

        if params.sort_by == SortOption.CODE_DESC:
            query = query.order_by(desc(Ward.code))
        elif params.sort_by == SortOption.CODE_ASC:
            query = query.order_by(asc(Ward.code))
        elif params.sort_by == SortOption.NAME_ASC:
            query = query.order_by(asc(Ward.name))
        elif params.sort_by == SortOption.NAME_DESC:
            query = query.order_by(desc(Ward.name))

        total_items = await db.execute(select(func.count()).select_from(query.subquery()))
        total_items = total_items.scalar()

        # Apply pagination
        offset = (params.page - 1) * params.size
        query = query.offset(offset).limit(params.size)

        result = await db.execute(query)
        items = result.scalars().all()

        return PaginatedWardsResponse(
            items=items,
            total_items=total_items,
            total_pages=(total_items // params.size) + (1 if total_items % params.size > 0 else 0),
            current_page=params.page
        )


wards = CRUDWards()
