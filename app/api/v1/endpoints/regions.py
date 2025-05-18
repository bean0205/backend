from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, require_role
from app.crud.crud_regions import regions
from app.schemas.regions import (
    RegionCreate,
    RegionOut,
)
from app.utils.role import Role
import logging

# Cấu hình logger mặc định
logging.basicConfig(level=logging.INFO)
router = APIRouter()


@router.post("/region", response_model=RegionOut,
             dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def create_region(
        region: RegionCreate,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Create a new region.
    """
    # check exist
    is_region_exist = await regions.get_by_code(db=db, code=region.code);
    if is_region_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Region with this code already exists"
        )
    # Create the region
    return await regions.create(db=db, obj_in=region)


@router.put("/region/{region_id}", response_model=RegionOut,
            dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def update_region(
        region_id: int,
        region: RegionCreate,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Update a region by ID.
    """
    # Check if the region exists
    existing_region = await regions.get_by_id(db=db, id=region_id)
    if not existing_region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region not found"
        )
    # Update the region
    return await regions.update(db=db, id=region_id, obj_in=region)


@router.get("/region/{region_id}", response_model=RegionOut, dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_region_by_id(
        region_id: int,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get a region by ID.
    """
    # Get the region
    region = await regions.get_by_id(db=db, id=region_id)
    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region not found"
        )
    return region


@router.delete("/region/{region_id}",
               dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def delete_region(
        region_id: int,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Delete a region by ID.
    """
    # Delete the region
    await regions.delete(db=db, id=region_id)
    return {"detail": "Region deleted successfully"}


@router.get("/paginated", dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_paginated_regions(
        page: int = Query(1, ge=1),
        size: int = Query(20, ge=1, le=100),
        search_term: Optional[str] = Query(None),
        sort_by: Optional[str] = Query(None),
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get a paginated list of regions.
    """
    # Get the paginated regions
    regions_list = await regions.get_paginated_regions(
        db=db,
        page=page,
        size=size,
        search_term=search_term,
        sort_by=sort_by
    )
    return regions_list
