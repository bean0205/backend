from datetime import timedelta
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, get_current_user, get_request_base_url
from app.core.config import settings
from app.core.security import create_access_token
from app.crud.crud_user import user
from app.db.models import User
from app.schemas.user import UserCreate, UserRead, Token, EmailSchema, ResetPasswordSchema
from app.services.email_service import EmailService

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    *,
    db: AsyncSession = Depends(get_db_session),
    user_in: UserCreate,
) -> Any:
    """
    Register a new user.
    """
    # Check if user with this email already exists
    db_user = await user.get_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email đã được sử dụng.",
        )
    
    # Create new user
    new_user = await user.create(db, obj_in=user_in)
    return new_user


@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # Authenticate user
    db_user = await user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not await user.is_active(db_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản không hoạt động.",
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=db_user.id, expires_delta=access_token_expires
    )
    
    # Return token and user data
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user,
    }


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout() -> Any:
    """
    Logout endpoint. This is optional and mainly for client-side logout.
    JWT tokens can't be invalidated server-side without a blacklist/database.
    """
    return {"message": "Đăng xuất thành công."}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    *,
    db: AsyncSession = Depends(get_db_session),
    email_in: EmailSchema,
    request: Request,
) -> Any:
    """
    Password recovery by email.
    """
    # Always return success to prevent email enumeration
    success_response = {
        "message": "Nếu email tồn tại, một liên kết đặt lại mật khẩu đã được gửi."
    }
    
    # Find user by email
    db_user = await user.get_by_email(db, email=email_in.email)
    if not db_user or not db_user.is_active:
        return success_response
    
    # Generate password reset token
    password_reset = await user.create_password_reset_token(db, user_id=db_user.id)
    
    # Get base URL from request
    base_url = get_request_base_url(request)
    
    # Send email with password reset link
    email_sent = await EmailService.send_password_reset_email(
        email_to=db_user.email,
        token=password_reset.token,
        base_url=base_url,
    )
    
    # Return success response regardless of email sending status
    # (but log the failure if email sending fails)
    return success_response


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    *,
    db: AsyncSession = Depends(get_db_session),
    reset_data: ResetPasswordSchema,
) -> Any:
    """
    Reset password using a valid token.
    """
    # Find valid token
    token_obj = await user.get_valid_password_reset_token(db, token=reset_data.token)
    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token không hợp lệ hoặc đã hết hạn.",
        )
    
    # Get user
    db_user = await user.get(db, user_id=token_obj.user_id)
    if not db_user or not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Người dùng không tồn tại hoặc không hoạt động.",
        )
    
    # Update password
    await user.update(db, db_obj=db_user, obj_in={"password": reset_data.new_password})
    
    # Mark token as used
    await user.use_password_reset_token(db, token_obj=token_obj)
    
    return {"message": "Mật khẩu đã được cập nhật thành công."}
