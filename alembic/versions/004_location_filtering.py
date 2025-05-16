"""Add location filtering related models

Revision ID: 004_location_filtering
Revises: 003_user_roles
Create Date: 2023-05-16 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2 as ga


# revision identifiers, used by Alembic.
revision: str = '004_location_filtering'
down_revision: Union[str, None] = '003_user_roles'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create countries table
    op.create_table('countries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('code', sa.String(length=2), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_countries_id'), 'countries', ['id'], unique=False)
    op.create_index(op.f('ix_countries_name'), 'countries', ['name'], unique=False)
    op.create_index(op.f('ix_countries_code'), 'countries', ['code'], unique=False)

    # Create regions table
    op.create_table('regions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('country_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_regions_id'), 'regions', ['id'], unique=False)
    op.create_index(op.f('ix_regions_name'), 'regions', ['name'], unique=False)

    # Create categories table
    op.create_table('categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=False)

    # Create amenities table
    op.create_table('amenities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('icon', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_amenities_id'), 'amenities', ['id'], unique=False)
    op.create_index(op.f('ix_amenities_name'), 'amenities', ['name'], unique=False)

    # Add columns to locations table
    op.add_column('locations', sa.Column('country_id', sa.Integer(), nullable=True))
    op.add_column('locations', sa.Column('region_id', sa.Integer(), nullable=True))
    op.add_column('locations', sa.Column('category_id', sa.Integer(), nullable=True))
    op.add_column('locations', sa.Column('thumbnail_url', sa.String(length=255), nullable=True))
    op.add_column('locations', sa.Column('price_min', sa.Float(), nullable=True))
    op.add_column('locations', sa.Column('price_max', sa.Float(), nullable=True))
    op.add_column('locations', sa.Column('popularity_score', sa.Float(), nullable=False, server_default='0.0'))
    
    # Add foreign key constraints
    op.create_foreign_key('fk_locations_country_id', 'locations', 'countries', ['country_id'], ['id'])
    op.create_foreign_key('fk_locations_region_id', 'locations', 'regions', ['region_id'], ['id'])
    op.create_foreign_key('fk_locations_category_id', 'locations', 'categories', ['category_id'], ['id'])
    
    # Create location_amenities table
    op.create_table('location_amenities',
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('amenity_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.ForeignKeyConstraint(['amenity_id'], ['amenities.id'], ),
        sa.PrimaryKeyConstraint('location_id', 'amenity_id')
    )
    
    # Create ratings table
    op.create_table('ratings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ratings_id'), 'ratings', ['id'], unique=False)
    
    # Migrate existing country data (from string to relation)
    op.execute("""
    UPDATE locations 
    SET country_id = c.id 
    FROM (
        SELECT id, name FROM countries
    ) as c 
    WHERE locations.country = c.name
    """)
    
    # Finally remove the now redundant country column
    op.drop_column('locations', 'country')


def downgrade() -> None:
    # Add back the country column
    op.add_column('locations', sa.Column('country', sa.String(length=100), nullable=True))
    
    # Migrate data back to the string column
    op.execute("""
    UPDATE locations 
    SET country = c.name 
    FROM (
        SELECT id, name FROM countries
    ) as c 
    WHERE locations.country_id = c.id
    """)
    
    # Drop all the tables in reverse order
    op.drop_index(op.f('ix_ratings_id'), table_name='ratings')
    op.drop_table('ratings')
    op.drop_table('location_amenities')
    
    # Remove foreign key constraints
    op.drop_constraint('fk_locations_category_id', 'locations', type_='foreignkey')
    op.drop_constraint('fk_locations_region_id', 'locations', type_='foreignkey')
    op.drop_constraint('fk_locations_country_id', 'locations', type_='foreignkey')
    
    # Remove added columns from locations
    op.drop_column('locations', 'popularity_score')
    op.drop_column('locations', 'price_max')
    op.drop_column('locations', 'price_min')
    op.drop_column('locations', 'thumbnail_url')
    op.drop_column('locations', 'category_id')
    op.drop_column('locations', 'region_id')
    op.drop_column('locations', 'country_id')
    
    # Drop amenities table
    op.drop_index(op.f('ix_amenities_name'), table_name='amenities')
    op.drop_index(op.f('ix_amenities_id'), table_name='amenities')
    op.drop_table('amenities')
    
    # Drop categories table
    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')
    
    # Drop regions table
    op.drop_index(op.f('ix_regions_name'), table_name='regions')
    op.drop_index(op.f('ix_regions_id'), table_name='regions')
    op.drop_table('regions')
    
    # Drop countries table
    op.drop_index(op.f('ix_countries_code'), table_name='countries')
    op.drop_index(op.f('ix_countries_name'), table_name='countries')
    op.drop_index(op.f('ix_countries_id'), table_name='countries')
    op.drop_table('countries')
