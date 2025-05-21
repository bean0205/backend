from typing import List, Optional, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models import (
    Continent, Country, Region, District, Ward,
    LocationCategory, Location
)
from app.schemas.location import (
    ContinentCreate, ContinentUpdate,
    CountryCreate, CountryUpdate,
    RegionCreate, RegionUpdate,
    DistrictCreate, DistrictUpdate,
    WardCreate, WardUpdate,
    LocationCategoryCreate, LocationCategoryUpdate,
    LocationCreate, LocationUpdate
)


class CRUDContinent(CRUDBase[Continent, ContinentCreate, ContinentUpdate]):
    async def get_by_code(self, db: AsyncSession, *, code: str) -> Optional[Continent]:
        result = await db.execute(select(Continent).filter(Continent.code == code))
        return result.scalars().first()

    async def get_all_active(self, db: AsyncSession) -> List[Continent]:
        result = await db.execute(select(Continent).filter(Continent.status == 1))
        return result.scalars().all()


class CRUDCountry(CRUDBase[Country, CountryCreate, CountryUpdate]):
    async def get_by_code(self, db: AsyncSession, *, code: str) -> Optional[Country]:
        result = await db.execute(select(Country).filter(Country.code == code))
        return result.scalars().first()

    async def get_by_continent(self, db: AsyncSession, *, continent_id: int) -> List[Country]:
        result = await db.execute(
            select(Country)
            .filter(Country.continent_id == continent_id)
            .filter(Country.status == 1)
        )
        return result.scalars().all()


class CRUDRegion(CRUDBase[Region, RegionCreate, RegionUpdate]):
    async def get_by_country(self, db: AsyncSession, *, country_id: int) -> List[Region]:
        result = await db.execute(
            select(Region)
            .filter(Region.country_id == country_id)
            .filter(Region.status == 1)
        )
        return result.scalars().all()


class CRUDDistrict(CRUDBase[District, DistrictCreate, DistrictUpdate]):
    async def get_by_region(self, db: AsyncSession, *, region_id: int) -> List[District]:
        result = await db.execute(
            select(District)
            .filter(District.region_id == region_id)
            .filter(District.status == 1)
        )
        return result.scalars().all()


class CRUDWard(CRUDBase[Ward, WardCreate, WardUpdate]):
    async def get_by_district(self, db: AsyncSession, *, district_id: int) -> List[Ward]:
        result = await db.execute(
            select(Ward)
            .filter(Ward.district_id == district_id)
            .filter(Ward.status == 1)
        )
        return result.scalars().all()


class CRUDLocationCategory(CRUDBase[LocationCategory, LocationCategoryCreate, LocationCategoryUpdate]):
    async def get_all_active(self, db: AsyncSession) -> List[LocationCategory]:
        result = await db.execute(
            select(LocationCategory).filter(LocationCategory.status == True)
        )
        return result.scalars().all()


class CRUDLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    async def get_by_category(
            self, db: AsyncSession, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Location]:
        result = await db.execute(
            select(Location)
            .filter(Location.category_id == category_id)
            .filter(Location.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_country(
            self, db: AsyncSession, *, country_id: int, skip: int = 0, limit: int = 100
    ) -> List[Location]:
        result = await db.execute(
            select(Location)
            .filter(Location.country_id == country_id)
            .filter(Location.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def search_locations(
            self,
            db: AsyncSession,
            *,
            search_term: str = None,
            country_id: int = None,
            region_id: int = None,
            district_id: int = None,
            category_id: int = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[Location]:
        query = select(Location).filter(Location.is_active == True)

        if search_term:
            query = query.filter(Location.name.ilike(f"%{search_term}%"))

        if country_id:
            query = query.filter(Location.country_id == country_id)

        if region_id:
            query = query.filter(Location.region_id == region_id)

        if district_id:
            query = query.filter(Location.district_id == district_id)

        if category_id:
            query = query.filter(Location.category_id == category_id)

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()


continent = CRUDContinent(Continent)
country = CRUDCountry(Country)
region = CRUDRegion(Region)
district = CRUDDistrict(District)
ward = CRUDWard(Ward)
location_category = CRUDLocationCategory(LocationCategory)
location = CRUDLocation(Location)
