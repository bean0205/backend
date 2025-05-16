"""Initial migration - Location table

Revision ID: 001_initial
Revises: 
Create Date: 2023-10-12 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2 as ga


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # First create PostGIS extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis')
    
    # Create the locations table
    op.create_table('locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('geom', ga.Geometry(geometry_type='POINT', srid=4326), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add indexes
    op.create_index(op.f('ix_locations_id'), 'locations', ['id'], unique=False)
    op.create_index(op.f('ix_locations_name'), 'locations', ['name'], unique=False)
    
    # Add spatial index for geometry column
    op.execute('CREATE INDEX idx_locations_geom ON locations USING GIST (geom)')


def downgrade() -> None:
    # Drop the table
    op.drop_index(op.f('ix_locations_name'), table_name='locations')
    op.drop_index(op.f('ix_locations_id'), table_name='locations')
    op.drop_index('idx_locations_geom', table_name='locations')
    op.drop_table('locations')
    
    # We don't remove the PostGIS extension as other tables might use it
