from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, get_current_user, require_role
from app.crud.crud_location import location
from app.db.models import User
from app.schemas.location import (
    Location, 
    LocationCreate, 
    LocationUpdate, 
    LocationList,
    LocationFilterParams,
    PaginatedLocationResponse,
    SortOption
)


router = APIRouter()


@router.get("/", response_model=PaginatedLocationResponse)
async def read_locations(
    db: AsyncSession = Depends(get_db_session),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    size: int = Query(20, ge=1, le=100, description="Page size, max 100"),
    search_term: Optional[str] = Query(None, description="Search term to filter by name, description, address"),
    country_id: Optional[int] = Query(None, description="Filter by country ID"),
    region_id: Optional[int] = Query(None, description="Filter by region ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    price_range_min: Optional[float] = Query(None, description="Filter by minimum price"),
    price_range_max: Optional[float] = Query(None, description="Filter by maximum price"),
    amenities: Optional[List[str]] = Query(None, description="Filter by amenities (comma-separated)"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Filter by minimum average rating"),
    sort_by: Optional[SortOption] = Query(None, description="Sort results by specified criteria"),
) -> Any:
    """
    Retrieve locations with advanced filtering, sorting, and pagination.
    
    - **page**: Page number, starting from 1
    - **size**: Number of items per page, max 100
    - **search_term**: Search term to filter by name, description, address
    - **country_id**: Filter by country ID
    - **region_id**: Filter by region ID
    - **category_id**: Filter by category ID
    - **price_range_min**: Filter by minimum price
    - **price_range_max**: Filter by maximum price
    - **amenities**: Filter by amenities (comma-separated)
    - **min_rating**: Filter by minimum average rating
    - **sort_by**: Sort results by specified criteria
    """
    # Create filter params object from query parameters
    filter_params = LocationFilterParams(
        page=page,
        size=size,
        search_term=search_term,
        country_id=country_id,
        region_id=region_id,
        category_id=category_id,
        price_range_min=price_range_min,
        price_range_max=price_range_max,
        amenities=amenities,
        min_rating=min_rating,
        sort_by=sort_by
    )
    
    # Get filtered locations
    locations_result, total_count, total_pages = await location.get_multi_filter(
        db=db, filter_params=filter_params
    )
    
    # Return paginated response
    return {
        "items": locations_result,
        "total_items": total_count,
        "total_pages": total_pages,
        "current_page": page
    }


@router.get("/legacy", response_model=LocationList)
async def read_locations_legacy(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> Any:
    """
    Legacy endpoint for backward compatibility.
    Retrieve locations with basic filtering.
    """
    filter_params = {}
    if search:
        filter_params["search"] = search
    if is_active is not None:
        filter_params["is_active"] = is_active
    
    items = await location.get_multi(
        db, skip=skip, limit=limit, filter_params=filter_params
    )
    total = await location.get_count(db, filter_params=filter_params)
    return {"items": items, "total": total}


@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(
    *,
    db: AsyncSession = Depends(get_db_session),
    location_in: LocationCreate,
    current_user: User = Depends(require_role("admin"))
) -> Any:
    """
    Create new location. Requires admin role.
    """
    return await location.create(db=db, obj_in=location_in)


@router.get("/{location_id}", response_model=Location)
async def read_location(
    *,
    db: AsyncSession = Depends(get_db_session),
    location_id: int,
    include_relations: bool = Query(False, description="Include related data like amenities and ratings"),
) -> Any:
    """
    Get location by ID with option to include related data.
    """
    result = await location.get(db=db, location_id=location_id, include_relations=include_relations)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    return result


@router.put("/{location_id}", response_model=Location)
async def update_location(
    *,
    db: AsyncSession = Depends(get_db_session),
    location_id: int,
    location_in: LocationUpdate,
    current_user: User = Depends(require_role("admin"))
) -> Any:
    """
    Update a location. Requires admin role.
    """
    result = await location.get(db=db, location_id=location_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    return await location.update(db=db, db_obj=result, obj_in=location_in)


@router.delete("/{location_id}", response_model=Location)
async def delete_location(
    *,
    db: AsyncSession = Depends(get_db_session),
    location_id: int,
    current_user: User = Depends(require_role("admin"))
) -> Any:
    """
    Delete a location. Requires admin role.
    """
    result = await location.get(db=db, location_id=location_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    return await location.delete(db=db, location_id=location_id)
    
    return await location.delete(db=db, location_id=location_id)
