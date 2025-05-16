from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, get_current_user, require_role
from app.crud.crud_location import location
from app.db.models import User
from app.schemas.location import Location, LocationCreate, LocationUpdate, LocationList


router = APIRouter()


@router.get("/", response_model=LocationList)
async def read_locations(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> Any:
    """
    Retrieve locations with optional filtering.
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
) -> Any:
    """
    Get location by ID.
    """
    result = await location.get(db=db, location_id=location_id)
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
