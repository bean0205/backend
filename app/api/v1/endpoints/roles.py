from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.db.models import User

router = APIRouter()


@router.get("/", response_model=List[schemas.Role])
async def read_roles(
        db: AsyncSession = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve roles with their permissions.
    """
    roles = await crud.role.get_multi(db, skip=skip, limit=limit)
    return roles


@router.post("/", response_model=schemas.Role)
async def create_role(
        *,
        db: AsyncSession = Depends(deps.get_db),
        role_in: schemas.RoleCreate,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new role with permissions.
    """
    # Check if role with this name already exists
    role = await crud.role.get_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role with this name already exists",
        )
    role = await crud.role.create(db, obj_in=role_in)
    return role


@router.get("/{role_id}", response_model=schemas.Role)
async def read_role(
        *,
        db: AsyncSession = Depends(deps.get_db),
        role_id: int,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get role by ID, including its permissions.
    """
    role = await crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return role


@router.put("/{role_id}", response_model=schemas.Role)
async def update_role(
        *,
        db: AsyncSession = Depends(deps.get_db),
        role_id: int,
        role_in: schemas.RoleUpdate,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a role and its permissions.
    """
    role = await crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    # If name is being updated, check that it doesn't conflict
    if role_in.name and role_in.name != role.name:
        existing = await crud.role.get_by_name(db, name=role_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role with this name already exists",
            )

    role = await crud.role.update(db, db_obj=role, obj_in=role_in)
    return role


@router.delete("/{role_id}", response_model=schemas.Role)
async def delete_role(
        *,
        db: AsyncSession = Depends(deps.get_db),
        role_id: int,
        current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a role.
    """
    role = await crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    # Check if role is assigned to any users before deleting
    users_with_role = await crud.user.get_by_role_id(db, role_id=role_id)
    if users_with_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete role, it is assigned to users",
        )

    role = await crud.role.remove(db, id=role_id)
    return role
