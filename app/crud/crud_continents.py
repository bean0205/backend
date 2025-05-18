from typing import List, Optional, Union, Dict, Any, Tuple

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc, and_, or_, Float

from app.db.models import Continent
from app.schemas.continents import (
    ContinentCreate,
    ContinentUpdate,
    PaginatedContinentsResponse,
    SortOption,
    PaginatedContinentsRequest
)


class CRUDContinents:
    async def get_by_code(self, db: AsyncSession, code: str) -> Optional[Continent]:
        """
        Get a continent by its code.
        """
        result = await db.execute(
            select(Continent).where(Continent.code == code)
        )
        return result.scalars().first()

    async def create(self, db: AsyncSession, obj_in: ContinentCreate) -> Continent:
        """
        Create a new continent.
        """
        continent = Continent(**obj_in.dict())
        db.add(continent)
        await db.commit()
        await db.refresh(continent)
        return continent

    async def get_all(self, db: AsyncSession) -> List[Continent]:
        """
        Get all continents.
        """
        result = await db.execute(
            select(Continent)
        )
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[Continent]:
        """
        Get a continent by its ID.
        """
        result = await db.execute(
            select(Continent).where(Continent.id == id)
        )
        return result.scalars().first()

    async def update(self, db: AsyncSession, db_obj: Continent, obj_in: ContinentUpdate) -> Continent:
        """
        Update a continent.
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> None:
        """
        Delete a continent by its ID.
        """
        continent = await self.get_by_id(db, id)
        if not continent:
            raise HTTPException(status_code=404, detail="Continent not found")
        await db.delete(continent)
        await db.commit()

    async def get_continents_by_pagination(
            self,
            db: AsyncSession,
            params: PaginatedContinentsRequest
    ) -> PaginatedContinentsResponse:
        """
        Get continents with pagination and filtering.
        """
        query = select(Continent)

        if params.search_term:
            query = query.where(
                or_(
                    Continent.name.ilike(f"%{params.search_term}%"),
                    Continent.code.ilike(f"%{params.search_term}%")
                )
            )

        if params.sort_by == SortOption.NAME_ASC:
            query = query.order_by(asc(Continent.name))
        elif params.sort_by == SortOption.NAME_DESC:
            query = query.order_by(desc(Continent.name))
        elif params.sort_by == SortOption.CODE_ASC:
            query = query.order_by(asc(Continent.code))
        elif params.sort_by == SortOption.CODE_DESC:
            query = query.order_by(desc(Continent.code))

        total_count = await db.execute(select(func.count()).select_from(query))
        total_count = total_count.scalar()

        if params.page and params.size:
            offset = (params.page - 1) * params.size
            query = query.offset(offset).limit(params.size)

        result = await db.execute(query)
        continents = result.scalars().all()

        return PaginatedContinentsResponse(
            items=continents,
            total_items=total_count,
            total_pages=(total_count // params.size) + (1 if total_count % params.size > 0 else 0),
            current_page=params.page if params.page else 1
        )


continents = CRUDContinents()
