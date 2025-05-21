from typing import List, Optional, Dict, Any, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.crud.permission import permission
from app.db.models import Role, Permission
from app.schemas.role import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Role]:
        """
        Get a role by name.
        """
        result = await db.execute(select(Role).filter(Role.name == name))
        return result.scalars().first()

    async def get_default_role(self, db: AsyncSession) -> Optional[Role]:
        """
        Get the default role.
        """
        result = await db.execute(select(Role).filter(Role.is_default == True))
        return result.scalars().first()

    async def get(self, db: AsyncSession, id: Any) -> Optional[Role]:
        """
        Get role by ID with permissions loaded.
        """
        result = await db.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .filter(Role.id == id)
        )
        return result.scalars().first()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Role]:
        """
        Get multiple roles with permissions loaded.
        """
        result = await db.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: RoleCreate) -> Role:
        """
        Create new role with permissions.
        """
        permission_ids = obj_in.permission_ids or []

        # Create role object without permissions first
        role_data = obj_in.dict(exclude={"permission_ids"})
        db_obj = Role(**role_data)

        # Add permissions if provided
        if permission_ids:
            permissions = await permission.get_multiple_by_ids(db, ids=permission_ids)
            db_obj.permissions = permissions

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self, db: AsyncSession, *, db_obj: Role, obj_in: Union[RoleUpdate, Dict[str, Any]]
    ) -> Role:
        """
        Update role and its permissions.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # Handle permission IDs separately
        permission_ids = update_data.pop("permission_ids", None)

        # Update role attributes
        await super().update(db, db_obj=db_obj, obj_in=update_data)

        # Update permissions if provided
        if permission_ids is not None:
            permissions = await permission.get_multiple_by_ids(db, ids=permission_ids)
            db_obj.permissions = permissions
            await db.commit()

        return db_obj


role = CRUDRole(Role)
