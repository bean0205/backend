from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models import MediaType, MediaCategory, Media
from app.schemas.media import (
    MediaTypeCreate, MediaTypeUpdate,
    MediaCategoryCreate, MediaCategoryUpdate,
    MediaCreate, MediaUpdate
)


class CRUDMediaType(CRUDBase[MediaType, MediaTypeCreate, MediaTypeUpdate]):
    async def get_all_active(self, db: AsyncSession) -> List[MediaType]:
        """Get all active media types"""
        result = await db.execute(
            select(MediaType).filter(MediaType.status == 1)
        )
        return result.scalars().all()


class CRUDMediaCategory(CRUDBase[MediaCategory, MediaCategoryCreate, MediaCategoryUpdate]):
    async def get_all_active(self, db: AsyncSession) -> List[MediaCategory]:
        """Get all active media categories"""
        result = await db.execute(
            select(MediaCategory).filter(MediaCategory.status == 1)
        )
        return result.scalars().all()


class CRUDMedia(CRUDBase[Media, MediaCreate, MediaUpdate]):
    async def get_by_reference(
            self,
            db: AsyncSession,
            *,
            reference_id: int,
            reference_type: str,
            skip: int = 0,
            limit: int = 100
    ) -> List[Media]:
        """Get media by reference ID and type"""
        result = await db.execute(
            select(Media)
            .filter(Media.reference_id == reference_id)
            .filter(Media.reference_type == reference_type)
            .filter(Media.status == 1)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_type(
            self,
            db: AsyncSession,
            *,
            type_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[Media]:
        """Get media by type ID"""
        result = await db.execute(
            select(Media)
            .filter(Media.type_id == type_id)
            .filter(Media.status == 1)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_category(
            self,
            db: AsyncSession,
            *,
            category_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[Media]:
        """Get media by category ID"""
        result = await db.execute(
            select(Media)
            .filter(Media.category_id == category_id)
            .filter(Media.status == 1)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


media_type = CRUDMediaType(MediaType)
media_category = CRUDMediaCategory(MediaCategory)
media = CRUDMedia(Media)
