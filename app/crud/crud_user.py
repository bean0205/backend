from typing import Optional, List, Union, Dict, Any
from datetime import datetime, timedelta

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import or_

from app.db.models import User, PasswordResetToken
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class CRUDUser:
    async def get(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get a user by email"""
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """Create a new user"""
        db_obj = User(
            email=obj_in.email,
            full_name=obj_in.full_name,
            hashed_password=get_password_hash(obj_in.password),
            is_active=True,
            role=obj_in.role,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """Update a user"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        # Handle password separately if it's in the update data
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        """Authenticate a user with email and password"""
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    async def is_active(self, user: User) -> bool:
        """Check if user is active"""
        return user.is_active
    
    async def is_superuser(self, user: User) -> bool:
        """Check if user is superuser"""
        return user.is_superuser
    
    async def create_password_reset_token(
        self, db: AsyncSession, user_id: int
    ) -> PasswordResetToken:
        """Create a password reset token for a user"""
        # First, invalidate any existing tokens
        query = select(PasswordResetToken).where(
            PasswordResetToken.user_id == user_id,
            PasswordResetToken.is_used == False,
            PasswordResetToken.expires_at > datetime.utcnow()
        )
        result = await db.execute(query)
        existing_tokens = result.scalars().all()
        
        for token in existing_tokens:
            token.is_used = True
        
        # Create a new token
        reset_token = PasswordResetToken.generate_token(user_id)
        db.add(reset_token)
        await db.commit()
        await db.refresh(reset_token)
        return reset_token
    
    async def get_valid_password_reset_token(
        self, db: AsyncSession, token: str
    ) -> Optional[PasswordResetToken]:
        """Get a valid password reset token"""
        query = select(PasswordResetToken).where(
            PasswordResetToken.token == token,
            PasswordResetToken.is_used == False,
            PasswordResetToken.expires_at > datetime.utcnow()
        )
        result = await db.execute(query)
        return result.scalars().first()
    
    async def use_password_reset_token(
        self, db: AsyncSession, token_obj: PasswordResetToken
    ) -> None:
        """Mark a password reset token as used"""
        token_obj.is_used = True
        await db.commit()


user = CRUDUser()
