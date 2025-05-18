from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, require_role
from app.crud.crud_wards import wards
from app.schemas.wards import (
    WardCreate,
    WardOut,
    PaginatedWardRequest
)
from app.utils.role import Role
import logging

# Cấu hình logger mặc định
logging.basicConfig(level=logging.INFO)
router = APIRouter()


@router.post("/ward", response_model=WardOut,
             dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def create_ward(
        ward: WardCreate,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Create a new ward.
    """
    # check exist
    is_ward_exist = await wards.get_by_code(db=db, code=ward.code)
    if is_ward_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ward with this code already exists"
        )
    # Create the ward
    return await wards.create(db=db, obj_in=ward)


@router.put("/ward/{ward_id}", response_model=WardOut,
            dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def update_ward(
        ward_id: int,
        ward: WardCreate,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Update a ward by ID.
    """
    # Check if the ward exists
    existing_ward = await wards.get_by_id(db=db, id=ward_id)
    if not existing_ward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ward not found"
        )
    # Update the ward
    return await wards.update(db=db, id=ward_id, obj_in=ward)


@router.get("/ward/{ward_id}", response_model=WardOut, dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_ward_by_id(
        ward_id: int,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get a ward by ID.
    """
    # Get the ward
    ward = await wards.get_by_id(db=db, id=ward_id)
    if not ward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ward not found"
        )
    return ward


@router.delete("/ward/{ward_id}",
               dependencies=[Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value]))])
async def delete_ward(
        ward_id: int,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Delete a ward by ID.
    """
    # Delete the ward
    await wards.delete(db=db, id=ward_id)
    return {"detail": "Ward deleted successfully"}


@router.get("/by-district/{district_id}", response_model=List[WardOut], dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_wards_by_district(
        district_id: int,
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get all wards for a specific district.
    """
    return await wards.get_by_district_id(db=db, district_id=district_id)


@router.get("/paginated", dependencies=[
    Depends(require_role([Role.SUPER_ADMIN.value, Role.ADMIN.value, Role.MODERATOR.value, Role.USER.value]))])
async def get_paginated_wards(
        page: int = Query(1, ge=1),
        size: int = Query(20, ge=1, le=100),
        search_term: Optional[str] = Query(None),
        sort_by: Optional[str] = Query(None),
        db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Get a paginated list of wards.
    """
    # Get the paginated wards
    params = PaginatedWardRequest(
        page=page,
        size=size,
        search_term=search_term,
        sort_by=sort_by
    )

    wards_list = await wards.get_paginated_wards(
        db=db,
        params=params
    )
    return wards_list
