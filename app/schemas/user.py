from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict, validator


# Base User Schema for shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True
    role: str = "user"  # Default role is "user"


# Schema for user creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str
    role: Optional[str] = "user"  # Default role is "user"
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter")
        return v


# Schema for user response
class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime


# Schema for updating user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None


# Login credentials schema
class LoginCredentials(BaseModel):
    email: EmailStr
    password: str


# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserRead


# Email schema for password reset
class EmailSchema(BaseModel):
    email: EmailStr


# Reset password schema
class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter")
        return v
