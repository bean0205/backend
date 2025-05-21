from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.db.models import User

router = APIRouter()


@router.get("/", response_model=List[schemas.Permission])
async def read_permissions(
        db: AsyncSession = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve permissions.
    """
    permissions = await crud.permission.get_multi(db, skip=skip, limit=limit)
    return permissions


@router.post("/", response_model=schemas.Permission)
async def create_permission(
        *,
        db: AsyncSession = Depends(deps.get_db),
        permission_in: schemas.PermissionCreate,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new permission.
    """
    # Check if permission with this code already exists
    permission = await crud.permission.get_by_code(db, code=permission_in.code)
    if permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission with this code already exists",
        )
    permission = await crud.permission.create(db, obj_in=permission_in)
    return permission


@router.get("/{permission_id}", response_model=schemas.Permission)
async def read_permission(
        *,
        db: AsyncSession = Depends(deps.get_db),
        permission_id: int,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get permission by ID.
    """
    permission = await crud.permission.get(db, id=permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
        )
    return permission


@router.put("/{permission_id}", response_model=schemas.Permission)
async def update_permission(
        *,
        db: AsyncSession = Depends(deps.get_db),
        permission_id: int,
        permission_in: schemas.PermissionUpdate,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a permission.
    """
    permission = await crud.permission.get(db, id=permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
        )

    # If code is being updated, check that it doesn't conflict
    if permission_in.code and permission_in.code != permission.code:
        existing = await crud.permission.get_by_code(db, code=permission_in.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission with this code already exists",
            )

    permission = await crud.permission.update(db, db_obj=permission, obj_in=permission_in)
    return permission


@router.delete("/{permission_id}", response_model=schemas.Permission)
async def delete_permission(
        *,
        db: AsyncSession = Depends(deps.get_db),
        permission_id: int,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a permission.
    """
    permission = await crud.permission.get(db, id=permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
        )
    permission = await crud.permission.remove(db, id=permission_id)
    return permission
