from typing import List, Optional, Dict, Any, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    async def get_by_code(self, db: AsyncSession, *, code: str) -> Optional[Permission]:
        """
        Get a permission by code.
        """
        result = await db.execute(select(Permission).filter(Permission.code == code))
        return result.scalars().first()

    async def get_multiple_by_ids(self, db: AsyncSession, *, ids: List[int]) -> List[Permission]:
        """
        Get multiple permissions by list of IDs.
        """
        result = await db.execute(select(Permission).filter(Permission.id.in_(ids)))
        return result.scalars().all()


permission = CRUDPermission(Permission)
