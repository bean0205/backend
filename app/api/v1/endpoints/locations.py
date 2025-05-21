from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.schemas.base import PaginationParams

router = APIRouter()


# Continent endpoints
@router.get("/continents/", response_model=List[schemas.Continent])
async def get_continents(
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve continents.
    """
    continents = await crud.continent.get_all_active(db)
    return continents


@router.get("/continents/{continent_id}", response_model=schemas.Continent)
async def get_continent(
        continent_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get continent by ID.
    """
    continent = await crud.continent.get(db, id=continent_id)
    if not continent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Continent not found",
        )
    return continent


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
@router.get("/countries/", response_model=List[schemas.Country])
async def get_countries(
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
        continent_id: Optional[int] = None,
) -> Any:
    """
    Retrieve countries. Filter by continent if provided.
    """
    if continent_id:
        countries = await crud.country.get_by_continent(db, continent_id=continent_id)
    else:
        countries = await crud.country.get_multi(db, skip=skip, limit=limit)
    return countries


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
@router.get("/regions/", response_model=List[schemas.Region])
async def get_regions(
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
        country_id: Optional[int] = None,
) -> Any:
    """
    Retrieve regions. Filter by country if provided.
    """
    if country_id:
        regions = await crud.region.get_by_country(db, country_id=country_id)
    else:
        regions = await crud.region.get_multi(db, skip=skip, limit=limit)
    return regions


@router.get("/regions/{region_id}", response_model=schemas.Region)
async def get_region(
        region_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get region by ID.
    """
    region = await crud.region.get(db, id=region_id)
    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region not found",
        )
    return region


@router.post("/regions/", response_model=schemas.Region)
async def create_region(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        region_in: schemas.RegionCreate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new region. Only for superusers.
    """
    region = await crud.region.create(db, obj_in=region_in)
    return region


@router.put("/regions/{region_id}", response_model=schemas.Region)
async def update_region(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        region_id: int,
        region_in: schemas.RegionUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a region. Only for superusers.
    """
    region = await crud.region.get(db, id=region_id)
    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region not found",
        )
    region = await crud.region.update(db, db_obj=region, obj_in=region_in)
    return region


# District endpoints - similar pattern to above
@router.get("/districts/", response_model=List[schemas.District])
async def get_districts(
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
        region_id: Optional[int] = None,
) -> Any:
    """
    Retrieve districts. Filter by region if provided.
    """
    if region_id:
        districts = await crud.district.get_by_region(db, region_id=region_id)
    else:
        districts = await crud.district.get_multi(db, skip=skip, limit=limit)
    return districts


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


# Ward endpoints - similar pattern
@router.get("/wards/", response_model=List[schemas.Ward])
async def get_wards(
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
        district_id: Optional[int] = None,
) -> Any:
    """
    Retrieve wards. Filter by district if provided.
    """
    if district_id:
        wards = await crud.ward.get_by_district(db, district_id=district_id)
    else:
        wards = await crud.ward.get_multi(db, skip=skip, limit=limit)
    return wards


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
@router.get("/location-categories/", response_model=List[schemas.LocationCategory])
async def get_location_categories(
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Retrieve all active location categories.
    """
    categories = await crud.location_category.get_all_active(db)
    return categories


@router.get("/location-categories/{category_id}", response_model=schemas.LocationCategory)
async def get_location_category(
        category_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get location category by ID.
    """
    category = await crud.location_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location category not found",
        )
    return category


@router.post("/location-categories/", response_model=schemas.LocationCategory)
async def create_location_category(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        category_in: schemas.LocationCategoryCreate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new location category. Only for superusers.
    """
    category = await crud.location_category.create(db, obj_in=category_in)
    return category


# Location endpoints
@router.get("/locations/", response_model=dict)
async def get_locations(
        db: AsyncSession = Depends(deps.get_db_session),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        search: Optional[str] = None,
        country_id: Optional[int] = None,
        region_id: Optional[int] = None,
        district_id: Optional[int] = None,
        category_id: Optional[int] = None,
) -> Any:
    """
    Search and retrieve locations with pagination and filters.
    """
    pagination_params = PaginationParams(page=page, limit=limit)

    locations = await crud.location.search_locations(
        db,
        search_term=search,
        country_id=country_id,
        region_id=region_id,
        district_id=district_id,
        category_id=category_id,
        skip=(page - 1) * limit,
        limit=limit
    )

    # Get total count for pagination info
    # This is a simplified version - in a real app, you would also count with the filters
    # and calculate total pages
    return {
        "items": locations,
        "total": len(locations),
        "page": page,
        "limit": limit,
        "pages": (len(locations) + limit - 1) // limit
    }


@router.get("/locations/{location_id}", response_model=schemas.Location)
async def get_location(
        location_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Get location by ID.
    """
    location = await crud.location.get(db, id=location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    return location


@router.post("/locations/", response_model=schemas.Location)
async def create_location(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        location_in: schemas.LocationCreate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new location. Only for superusers.
    """
    location = await crud.location.create(db, obj_in=location_in)
    return location


@router.put("/locations/{location_id}", response_model=schemas.Location)
async def update_location(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        location_id: int,
        location_in: schemas.LocationUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a location. Only for superusers.
    """
    location = await crud.location.get(db, id=location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    location = await crud.location.update(db, db_obj=location, obj_in=location_in)
    return location
