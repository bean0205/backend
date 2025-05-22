from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.utils.role import get_default_role_id

router = APIRouter()


@router.post("/register", response_model=schemas.UserRegisterResponse)
async def register(
        user_in: schemas.UserCreate,
        db: AsyncSession = Depends(deps.get_db_session)
) -> Any:
    """
    Create new user account and return access token
    """
    # Check if email already exists
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # If role_id not provided, assign default role
    if not user_in.role_id:
        default_role_id = await get_default_role_id(db)
        user_in.role_id = default_role_id

    # Create new user
    new_user = await crud.user.create(db, obj_in=user_in)

    # Generate access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        new_user.id, expires_delta=access_token_expires
    )

    # Return user info and token
    return {
        "user": new_user,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=schemas.Token)
async def login_access_token(
        db: AsyncSession = Depends(deps.get_db_session),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/password-reset", response_model=schemas.Token)
async def request_password_reset(
        password_reset: schemas.PasswordReset,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Request a password reset token
    """
    user = await crud.user.get_by_email(db, email=password_reset.email)
    if user:
        # In a real app, send the token via email
        # For now, we'll just return it directly
        token = security.generate_password_reset_token(user.email)
        # Here we would send an email with the token
        return {"access_token": token, "token_type": "bearer"}
    # Always return success to avoid leaking which emails are registered
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/password-reset/confirm", response_model=schemas.Token)
async def reset_password_confirm(
        password_reset: schemas.PasswordResetConfirm,
        db: AsyncSession = Depends(deps.get_db_session),
) -> Any:
    """
    Reset a user's password using a password reset token
    """
    email = security.verify_password_reset_token(password_reset.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = await crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    hashed_password = security.get_password_hash(password_reset.password)
    user.hashed_password = hashed_password
    db.add(user)
    await db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
