from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app import crud, schemas
from app.api import deps
from app.schemas.base import PaginationParams
from app.db.models import Continent, Country, Region, District, Ward, LocationCategory

router = APIRouter()


# Continent endpoints
@router.get("/continents/", response_model=schemas.PaginatedResponse)
async def get_continents(
        db: AsyncSession = Depends(deps.get_db_session),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        all: bool = False,
) -> Any:
    """
    Retrieve continents with pagination.
    Set all=true to retrieve all items without pagination.
    """
    if all:
        continents_db = await crud.continent.get_all_active(db)
        # Convert SQLAlchemy models to Pydantic schemas
        continents = [schemas.Continent.model_validate(continent) for continent in continents_db]
        return {
            "items": continents,
            "total": len(continents),
            "page": 1,
            "limit": len(continents),
            "pages": 1
        }

    skip = (page - 1) * limit

    # Get total count
    total_count_query = select(func.count(Continent.id)).where(Continent.status == 1)
    total_count_result = await db.execute(total_count_query)
    total_count = total_count_result.scalar() or 0

    # Get paginated items
    query = select(Continent).filter(Continent.status == 1).offset(skip).limit(limit)
    result = await db.execute(query)
    continents_db = result.scalars().all()
    # Convert SQLAlchemy models to Pydantic schemas
    continents = [schemas.Continent.model_validate(continent) for continent in continents_db]

    # Calculate total pages
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0

    return {
        "items": continents,
        "total": total_count,
        "page": page,
        "limit": limit,
        "pages": total_pages
    }


@router.get("/continents/{continent_id}", response_model=schemas.ContinentWithCountries)
async def get_continent(
        continent_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get continent by ID with its list of countries.
    """
    continent = await crud.continent.get(db, id=continent_id)
    if not continent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Continent not found",
        )

    # Get countries belonging to this continent
    countries = await crud.country.get_by_continent(db, continent_id=continent_id)

    # Create response with continent data and countries
    response = schemas.ContinentWithCountries(
        **continent.__dict__,
        countries=countries
    )

    return response


@router.post("/continents/", response_model=schemas.Continent)
async def create_continent(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        continent_in: schemas.ContinentCreate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new continent. Only for superusers.
    """
    continent = await crud.continent.create(db, obj_in=continent_in)
    return continent


@router.put("/continents/{continent_id}", response_model=schemas.Continent)
async def update_continent(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        continent_id: int,
        continent_in: schemas.ContinentUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a continent. Only for superusers.
    """
    continent = await crud.continent.get(db, id=continent_id)
    if not continent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Continent not found",
        )
    continent = await crud.continent.update(db, db_obj=continent, obj_in=continent_in)
    return continent


# Country endpoints
@router.get("/countries/", response_model=schemas.PaginatedResponse)
async def get_countries(
        db: AsyncSession = Depends(deps.get_db_session),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        continent_id: Optional[int] = None,
        all: bool = False,
) -> Any:
    """
    Retrieve countries with pagination. Filter by continent if provided.
    Set all=true to retrieve all items without pagination.
    """
    if all:
        if continent_id:
            countries_db = await crud.country.get_by_continent(db, continent_id=continent_id)
        else:
            # Get all countries
            result = await db.execute(select(Country).filter(Country.status == 1))
            countries_db = result.scalars().all()

        # Convert SQLAlchemy models to Pydantic schemas
        countries = [schemas.Country.model_validate(country) for country in countries_db]

        return {
            "items": countries,
            "total": len(countries),
            "page": 1,
            "limit": len(countries),
            "pages": 1
        }

    skip = (page - 1) * limit

    # Get total count based on filters
    count_query = select(func.count(Country.id)).where(Country.status == 1)
    if continent_id:
        count_query = count_query.filter(Country.continent_id == continent_id)

    total_count_result = await db.execute(count_query)
    total_count = total_count_result.scalar() or 0

    # Get paginated items
    if continent_id:
        # This is a simplified approach - for large datasets,
        # we should modify get_by_continent to accept skip/limit
        result = await db.execute(
            select(Country)
            .filter(Country.continent_id == continent_id)
            .filter(Country.status == 1)
            .offset(skip).limit(limit)
        )
        countries_db = result.scalars().all()
        # Convert SQLAlchemy models to Pydantic schemas
        countries = [schemas.Country.model_validate(country) for country in countries_db]
    else:
        countries_db = await crud.country.get_multi(db, skip=skip, limit=limit)
        # Convert SQLAlchemy models to Pydantic schemas
        countries = [schemas.Country.model_validate(country) for country in countries_db]

    # Calculate total pages
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0

    return {
        "items": countries,
        "total": total_count,
        "page": page,
        "limit": limit,
        "pages": total_pages
    }


@router.get("/countries/{country_id}", response_model=schemas.Country)
async def get_country(
        country_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get country by ID.
    """
    country = await crud.country.get(db, id=country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found",
        )
    return country


@router.post("/countries/", response_model=schemas.Country)
async def create_country(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        country_in: schemas.CountryCreate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new country. Only for superusers.
    """
    country = await crud.country.create(db, obj_in=country_in)
    return country


@router.put("/countries/{country_id}", response_model=schemas.Country)
async def update_country(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        country_id: int,
        country_in: schemas.CountryUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a country. Only for superusers.
    """
    country = await crud.country.get(db, id=country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found",
        )
    country = await crud.country.update(db, db_obj=country, obj_in=country_in)
    return country


# Region endpoints
@router.get("/regions/", response_model=schemas.PaginatedResponse)
async def get_regions(
        db: AsyncSession = Depends(deps.get_db_session),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        country_id: Optional[int] = None,
        all: bool = False,
) -> Any:
    """
    Retrieve regions with pagination. Filter by country if provided.
    Set all=true to retrieve all items without pagination.
    """
    if all:
        if country_id:
            regions_db = await crud.region.get_by_country(db, country_id=country_id)
        else:
            # Get all regions
            result = await db.execute(select(Region).filter(Region.status == 1))
            regions_db = result.scalars().all()

        # Convert SQLAlchemy models to Pydantic schemas
        regions = [schemas.Region.model_validate(region) for region in regions_db]

        return {
            "items": regions,
            "total": len(regions),
            "page": 1,
            "limit": len(regions),
            "pages": 1
        }

    skip = (page - 1) * limit

    # Get total count based on filters
    count_query = select(func.count(Region.id)).where(Region.status == 1)
    if country_id:
        count_query = count_query.filter(Region.country_id == country_id)

    total_count_result = await db.execute(count_query)
    total_count = total_count_result.scalar() or 0

    # Get paginated items
    if country_id:
        result = await db.execute(
            select(Region)
            .filter(Region.country_id == country_id)
            .filter(Region.status == 1)
            .offset(skip).limit(limit)
        )
        regions_db = result.scalars().all()
    else:
        regions_db = await crud.region.get_multi(db, skip=skip, limit=limit)

    # Convert SQLAlchemy models to Pydantic schemas
    regions = [schemas.Region.model_validate(region) for region in regions_db]

    # Calculate total pages
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0

    return {
        "items": regions,
        "total": total_count,
        "page": page,
        "limit": limit,
        "pages": total_pages
    }


# District endpoints
@router.get("/districts/", response_model=schemas.PaginatedResponse)
async def get_districts(
        db: AsyncSession = Depends(deps.get_db_session),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        region_id: Optional[int] = None,
        all: bool = False,
) -> Any:
    """
    Retrieve districts with pagination. Filter by region if provided.
    Set all=true to retrieve all items without pagination.
    """
    if all:
        if region_id:
            districts_db = await crud.district.get_by_region(db, region_id=region_id)
        else:
            # Get all districts
            result = await db.execute(select(District).filter(District.status == 1))
            districts_db = result.scalars().all()

        # Convert SQLAlchemy models to Pydantic schemas
        districts = [schemas.District.model_validate(district) for district in districts_db]

        return {
            "items": districts,
            "total": len(districts),
            "page": 1,
            "limit": len(districts),
            "pages": 1
        }

    skip = (page - 1) * limit

    # Get total count based on filters
    count_query = select(func.count(District.id)).where(District.status == 1)
    if region_id:
        count_query = count_query.filter(District.region_id == region_id)

    total_count_result = await db.execute(count_query)
    total_count = total_count_result.scalar() or 0

    # Get paginated items
    if region_id:
        result = await db.execute(
            select(District)
            .filter(District.region_id == region_id)
            .filter(District.status == 1)
            .offset(skip).limit(limit)
        )
        districts_db = result.scalars().all()
    else:
        districts_db = await crud.district.get_multi(db, skip=skip, limit=limit)

    # Convert SQLAlchemy models to Pydantic schemas
    districts = [schemas.District.model_validate(district) for district in districts_db]

    # Calculate total pages
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0

    return {
        "items": districts,
        "total": total_count,
        "page": page,
        "limit": limit,
        "pages": total_pages
    }


@router.get("/districts/{district_id}", response_model=schemas.District)
async def get_district(
        district_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get district by ID.
    """
    district = await crud.district.get(db, id=district_id)
    if not district:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District not found",
        )
    return district


# Ward endpoints
@router.get("/wards/", response_model=schemas.PaginatedResponse)
async def get_wards(
        db: AsyncSession = Depends(deps.get_db_session),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        district_id: Optional[int] = None,
        all: bool = False,
) -> Any:
    """
    Retrieve wards with pagination. Filter by district if provided.
    Set all=true to retrieve all items without pagination.
    """
    if all:
        if district_id:
            wards_db = await crud.ward.get_by_district(db, district_id=district_id)
        else:
            # Get all wards
            result = await db.execute(select(Ward).filter(Ward.status == 1))
            wards_db = result.scalars().all()

        # Convert SQLAlchemy models to Pydantic schemas
        wards = [schemas.Ward.model_validate(ward) for ward in wards_db]

        return {
            "items": wards,
            "total": len(wards),
            "page": 1,
            "limit": len(wards),
            "pages": 1
        }

    skip = (page - 1) * limit

    # Get total count based on filters
    count_query = select(func.count(Ward.id)).where(Ward.status == 1)
    if district_id:
        count_query = count_query.filter(Ward.district_id == district_id)

    total_count_result = await db.execute(count_query)
    total_count = total_count_result.scalar() or 0

    # Get paginated items
    if district_id:
        result = await db.execute(
            select(Ward)
            .filter(Ward.district_id == district_id)
            .filter(Ward.status == 1)
            .offset(skip).limit(limit)
        )
        wards_db = result.scalars().all()
    else:
        wards_db = await crud.ward.get_multi(db, skip=skip, limit=limit)

    # Convert SQLAlchemy models to Pydantic schemas
    wards = [schemas.Ward.model_validate(ward) for ward in wards_db]

    # Calculate total pages
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0

    return {
        "items": wards,
        "total": total_count,
        "page": page,
        "limit": limit,
        "pages": total_pages
    }


@router.get("/wards/{ward_id}", response_model=schemas.Ward)
async def get_ward(
        ward_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get ward by ID.
    """
    ward = await crud.ward.get(db, id=ward_id)
    if not ward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ward not found",
        )
    return ward


# Location Category endpoints
@router.get("/location-categories/", response_model=schemas.PaginatedResponse)
async def get_location_categories(
        db: AsyncSession = Depends(deps.get_db_session),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        all: bool = False,
) -> Any:
    """
    Retrieve location categories with pagination.
    Set all=true to retrieve all items without pagination.
    """
    if all:
        categories_db = await crud.location_category.get_all_active(db)
        # Convert SQLAlchemy models to Pydantic schemas
        categories = [schemas.LocationCategory.model_validate(category) for category in categories_db]
        return {
            "items": categories,
            "total": len(categories),
            "page": 1,
            "limit": len(categories),
            "pages": 1
        }

    skip = (page - 1) * limit

    # Get total count
    count_query = select(func.count(LocationCategory.id)).where(LocationCategory.status == True)
    total_count_result = await db.execute(count_query)
    total_count = total_count_result.scalar() or 0

    # Get paginated items
    query = select(LocationCategory).filter(LocationCategory.status == True).offset(skip).limit(limit)
    result = await db.execute(query)
    categories_db = result.scalars().all()
    # Convert SQLAlchemy models to Pydantic schemas
    categories = [schemas.LocationCategory.model_validate(category) for category in categories_db]

    # Calculate total pages
    total_pages = (total_count + limit - 1) // limit if limit > 0 else 0

    return {
        "items": categories,
        "total": total_count,
        "page": page,
        "limit": limit,
        "pages": total_pages
    }
