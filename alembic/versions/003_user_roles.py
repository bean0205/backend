"""Add role field to users table

Revision ID: 003_user_roles
Revises: 002_user_auth
Create Date: 2023-05-16 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_user_roles'
down_revision: Union[str, None] = '002_user_auth'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add role column to users table with default value 'user'
    op.add_column('users', sa.Column('role', sa.String(length=50), nullable=False, server_default='user'))


def downgrade() -> None:
    # Drop role column from users table
    op.drop_column('users', 'role')
