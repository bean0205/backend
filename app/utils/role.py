from enum import Enum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Role as RoleModel


class Role(Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "supper_admin"


async def get_default_role_id(db: AsyncSession) -> int:
    """
    Get the ID of the default user role.
    If a role with is_default=True exists, return its ID.
    Otherwise, look for a role with name 'user'.
    If neither exists, return the first role found or raise an exception.
    """
    # First try to find a role with is_default=True
    result = await db.execute(select(RoleModel).filter(RoleModel.is_default == True))
    default_role = result.scalars().first()

    if default_role:
        return default_role.id

    # If no default role is found, try to find the 'user' role
    result = await db.execute(select(RoleModel).filter(RoleModel.name == Role.USER.value))
    user_role = result.scalars().first()

    if user_role:
        return user_role.id

    # If still no role is found, get the first role or raise an exception
    result = await db.execute(select(RoleModel))
    any_role = result.scalars().first()

    if not any_role:
        raise ValueError("No roles found in the database. Please create at least one role.")

    return any_role.id
