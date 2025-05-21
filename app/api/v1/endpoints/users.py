from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.core.security import get_password_hash

router = APIRouter()


@router.get("/me", response_model=schemas.User)
async def read_current_user(
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user information
    """
    return current_user


@router.put("/me", response_model=schemas.User)
async def update_current_user(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        user_in: schemas.UserUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update current user information
    """
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.put("/me/password", response_model=schemas.User)
async def update_password(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        password_change: schemas.PasswordChange,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update current user password
    """
    # Verify current password
    if not crud.user.authenticate(db, email=current_user.email, password=password_change.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    # Update password
    user_in = schemas.UserUpdate(password=password_change.new_password)
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/", response_model=List[schemas.User])
async def read_users(
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users. Only for superusers.
    """
    users = await crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
async def create_user(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        user_in: schemas.UserCreate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user. Only for superusers.
    """
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
        user_id: int,
        db: AsyncSession = Depends(deps.get_db_session),
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific user by id.
    Normal users can only get their own user.
    Superusers can get any user.
    """
    user = await crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        user_id: int,
        user_in: schemas.UserUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user. Only for superusers.
    """
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
