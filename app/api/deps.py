from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import get_db
from app.db.models import User
from app import crud
import logging

# Cấu hình logger mặc định
logging.basicConfig(level=logging.INFO)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


# Dependency to get the database session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db():
        yield session


async def get_current_user(
        db: AsyncSession = Depends(get_db_session),
        token: str = Depends(oauth2_scheme),
) -> User:
    """
    Get the current user based on the provided JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception

    # Get user from database
    user_obj = await crud.user.get(db, id=int(user_id))
    if user_obj is None:
        raise credentials_exception

    # Check if user is active
    if not user_obj.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return user_obj


async def get_current_active_user(
        current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current active user.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return current_user


async def get_current_active_superuser(
        current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current active superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không đủ quyền hạn.",
        )

    return current_user


def require_role(required_role: list[str]):
    """
    Dependency to check if the current user has the required role.
    """

    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.role in required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient privileges. Required role: {required_role}",
            )
        return current_user

    return role_checker


def get_request_base_url(request: Request) -> str:
    """
    Get the base URL from the request.
    """
    server_host = request.headers.get("host", "localhost")
    scheme = request.headers.get("x-forwarded-proto", "http")
    return f"{scheme}://{server_host}"
