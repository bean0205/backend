from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, require_role, get_current_user
from app.crud.crud_location import location
from app.db.models import User
from app.schemas.location import (
    LocationCreate,
    LocationUpdate,
    LocationOut,
    LocationFilterParams,
    PaginatedLocationResponse,
    NearbyLocationRequest
)
from app.utils.role import Role
import logging

# Cấu hình logger mặc định
logging.basicConfig(level=logging.INFO)
router = APIRouter()


@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value]))])
async def create_location(
        location_in: LocationCreate,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Create a new location.

    Requires admin or moderator role.
    """
    try:
        return await location.create(db=db, obj_in=location_in)
    except Exception as e:
        logging.error(f"Error creating location: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create location: {str(e)}"
        )


@router.get("/{location_id}", response_model=LocationOut)
async def get_location(
        location_id: int = Path(..., title="The ID of the location to get"),
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get a location by ID.
    """
    result = await location.get_by_id(db=db, id=location_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    return result


@router.put("/{location_id}", response_model=LocationOut,
            dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value]))])
async def update_location(
        location_in: LocationUpdate,
        location_id: int = Path(..., title="The ID of the location to update"),
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Update a location.

    Requires admin or moderator role.
    """
    try:
        return await location.update(db=db, id=location_id, obj_in=location_in)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating location: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update location: {str(e)}"
        )


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def delete_location(
        location_id: int = Path(..., title="The ID of the location to delete"),
        db: AsyncSession = Depends(get_db_session)
) -> None:
    """
    Delete a location.

    Requires admin role.
    """
    try:
        await location.delete(db=db, id=location_id)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting location: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete location: {str(e)}"
        )


@router.post("/search", response_model=PaginatedLocationResponse)
async def search_locations(
        params: LocationFilterParams = Body(...),
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Search and filter locations.
    """
    try:
        return await location.filter_locations(db=db, params=params)
    except Exception as e:
        logging.error(f"Error searching locations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search locations: {str(e)}"
        )


@router.post("/nearby", response_model=List[LocationOut])
async def find_nearby_locations(
        params: NearbyLocationRequest,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Find locations near a specified point.

    Args:
        params: Includes latitude, longitude, radius (in km), and optional category_id
    """
    try:
        nearby_locations = await location.find_nearby_locations(
            db=db,
            latitude=params.latitude,
            longitude=params.longitude,
            radius=params.radius,
            limit=params.limit,
            category_id=params.category_id
        )
        return nearby_locations
    except Exception as e:
        logging.error(f"Error finding nearby locations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to find nearby locations: {str(e)}"
        )
