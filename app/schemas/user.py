from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import BaseSchema, TimestampMixin


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True
    role: str = "user"


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None


class User(UserBase, TimestampMixin, BaseSchema):
    id: int
    is_superuser: bool = False


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    password: str = Field(..., min_length=8)


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


class PasswordResetTokenBase(BaseModel):
    token: str
    user_id: int
    expires_at: datetime
    is_used: bool = False


class PasswordResetTokenCreate(PasswordResetTokenBase):
    pass


class PasswordResetToken(PasswordResetTokenBase, TimestampMixin, BaseSchema):
    id: int
