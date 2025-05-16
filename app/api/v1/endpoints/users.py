from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, require_role
from app.crud.crud_user import user
from app.db.models import User
from app.schemas.user import UserRead, UserUpdate


router = APIRouter()


@router.get("/", response_model=List[UserRead])
async def read_users(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_role("admin"))
) -> Any:
    """
    Retrieve users. Requires admin role.
    """
    # Execute a simple query to get users with pagination
    users = []
    async for session in get_db_session():
        query = session.query(User).offset(skip).limit(limit)
        result = await session.execute(query)
        users = result.scalars().all()
    
    return users


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    *,
    db: AsyncSession = Depends(get_db_session),
    user_id: int,
    current_user: User = Depends(require_role("admin"))
) -> Any:
    """
    Get a specific user by ID. Requires admin role.
    """
    db_user = await user.get(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )
    return db_user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    *,
    db: AsyncSession = Depends(get_db_session),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(require_role("admin"))
) -> Any:
    """
    Update a user. Requires admin role.
    """
    db_user = await user.get(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )
    
    # Update user
    updated_user = await user.update(db=db, db_obj=db_user, obj_in=user_in)
    return updated_user
