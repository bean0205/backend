from typing import List, Optional, Union, Dict, Any, Tuple

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc, and_, or_, Float

from app.db.models import Country
from app.schemas.countries import CountryCreate, CountryUpdate, PaginatedCountriesResponse, SortOption, \
    PaginatedCountriesRequest


class CRUDCountries:
    async def get_by_code(self, db: AsyncSession, code: str) -> Optional[Country]:
        """
        Get a country by its code.
        """
        result = await db.execute(
            select(Country).where(Country.code == code)
        )
        return result.scalars().first()

    async def create(self, db: AsyncSession, obj_in: CountryCreate) -> Country:
        """
        Create a new country.
        """
        country = Country(**obj_in.dict())
        db.add(country)
        await db.commit()
        await db.refresh(country)
        return country

    async def get_all(self, db: AsyncSession) -> List[Country]:
        """
        Get all countries.
        """
        result = await db.execute(
            select(Country)
        )
        return result.scalars().all()

    async def get_by_continent_id(self, db: AsyncSession, continent_id: int) -> List[Country]:
        """
        Get all countries for a specific continent.
        """
        result = await db.execute(
            select(Country).where(Country.continent_id == continent_id)
        )
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[Country]:
        """
        Get a country by its ID.
        """
        result = await db.execute(
            select(Country).where(Country.id == id)
        )
        return result.scalars().first()

    async def update(self, db: AsyncSession, db_obj: Country, obj_in: CountryUpdate) -> Country:
        """
        Update a country.
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
        Delete a country by its ID.
        """
        country = await self.get_by_id(db, id)
        if not country:
            raise HTTPException(status_code=404, detail="Country not found")
        await db.delete(country)
        await db.commit()

    async def get_countries_by_pagination(
            self,
            db: AsyncSession,
            params: PaginatedCountriesRequest
    ) -> PaginatedCountriesResponse:
        """
        Get countries with pagination and filtering.
        """
        query = select(Country)

        if params.search_term:
            query = query.where(
                or_(
                    Country.name.ilike(f"%{params.search_term}%"),
                    Country.code.ilike(f"%{params.search_term}%")
                )
            )

        if params.continent_id:
            query = query.where(Country.continent_id == params.continent_id)

        if params.sort_by == SortOption.NAME_ASC:
            query = query.order_by(asc(Country.name))
        elif params.sort_by == SortOption.NAME_DESC:
            query = query.order_by(desc(Country.name))
        elif params.sort_by == SortOption.CODE_ASC:
            query = query.order_by(asc(Country.code))
        elif params.sort_by == SortOption.CODE_DESC:
            query = query.order_by(desc(Country.code))

        total_count = await db.execute(select(func.count()).select_from(query))
        total_count = total_count.scalar()

        if params.page and params.size:
            offset = (params.page - 1) * params.size
            query = query.offset(offset).limit(params.size)

        result = await db.execute(query)
        countries = result.scalars().all()

        return PaginatedCountriesResponse(
            items=countries,
            total_items=total_count,
            total_pages=(total_count // params.size) + (1 if total_count % params.size > 0 else 0),
            current_page=params.page if params.page else 1
        )


countries = CRUDCountries()
