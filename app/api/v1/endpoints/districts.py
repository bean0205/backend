from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, require_role
from app.crud.crud_districts import districts
from app.schemas.districts import (
    DistrictCreate,
    DistrictOut,
    PaginatedDistrictRequest
)
from app.utils.role import Role
import logging

# Cấu hình logger mặc định
logging.basicConfig(level=logging.INFO)
router = APIRouter()


@router.post("/district", response_model=DistrictOut,
             dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def create_district(
        district: DistrictCreate,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Create a new district.
    """
    # check exist
    is_district_exist = await districts.get_by_code(db=db, code=district.code)
    if is_district_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="District with this code already exists"
        )
    # Create the district
    return await districts.create(db=db, obj_in=district)


@router.put("/district/{district_id}", response_model=DistrictOut,
            dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def update_district(
        district_id: int,
        district: DistrictCreate,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Update a district by ID.
    """
    # Check if the district exists
    existing_district = await districts.get_by_id(db=db, id=district_id)
    if not existing_district:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District not found"
        )
    # Update the district
    return await districts.update(db=db, id=district_id, obj_in=district)


@router.get("/district/{district_id}", response_model=DistrictOut, dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_district_by_id(
        district_id: int,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get a district by ID.
    """
    # Get the district
    district = await districts.get_by_id(db=db, id=district_id)
    if not district:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District not found"
        )
    return district


@router.delete("/district/{district_id}",
               dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def delete_district(
        district_id: int,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Delete a district by ID.
    """
    # Delete the district
    await districts.delete(db=db, id=district_id)
    return {"detail": "District deleted successfully"}


@router.get("/by-region/{region_id}", response_model=List[DistrictOut], dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_districts_by_region(
        region_id: int,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get all districts for a specific region.
    """
    return await districts.get_by_region_id(db=db, region_id=region_id)


@router.get("/paginated", dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_paginated_districts(
        page: int = Query(1, ge=1),
        size: int = Query(20, ge=1, le=100),
        search_term: Optional[str] = Query(None),
        sort_by: Optional[str] = Query(None),
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get a paginated list of districts.
    """
    # Get the paginated districts
    params = PaginatedDistrictRequest(
        page=page,
        size=size,
        search_term=search_term,
        sort_by=sort_by
    )

    districts_list = await districts.get_paginated_districts(
        db=db,
        params=params
    )
    return districts_list
