# This script initializes alembic commands
# You can add custom commands here if needed

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = 'init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String(255), unique=True, index=True),
        sa.Column('full_name', sa.String(255)),
        sa.Column('hashed_password', sa.String(255)),
        sa.Column('role', sa.String(50), default='user'),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_superuser', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )

    op.create_table(
        'password_reset_tokens',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('token', sa.String(255), unique=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('expires_at', sa.DateTime),
        sa.Column('is_used', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now())
    )

    op.create_table(
        'continents',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(100), unique=True, index=True),
        sa.Column('code', sa.String(10), unique=True, index=True)
    )

    op.create_table(
        'countries',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('code', sa.String(10), unique=True, index=True),
        sa.Column('name', sa.String(100), index=True),
        sa.Column('continent_id', sa.Integer, sa.ForeignKey('continents.id', ondelete='CASCADE'))
    )

    op.create_table(
        'regions',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(100), index=True),
        sa.Column('code', sa.String(10), unique=True, index=True),
        sa.Column('country_id', sa.Integer, sa.ForeignKey('countries.id', ondelete='CASCADE'))
    )

    op.create_table(
        'districts',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(100), index=True),
        sa.Column('code', sa.String(10), unique=True, index=True),
        sa.Column('region_id', sa.Integer, sa.ForeignKey('regions.id', ondelete='CASCADE'))
    )

    op.create_table(
        'wards',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(100), index=True),
        sa.Column('code', sa.String(10), unique=True, index=True),
        sa.Column('district_id', sa.Integer, sa.ForeignKey('districts.id', ondelete='CASCADE'))
    )

    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(100), unique=True, index=True)
    )

    op.create_table(
        'locations',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(255), index=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('latitude', sa.Float, nullable=False),
        sa.Column('longitude', sa.Float, nullable=False),
        sa.Column('geom', Geometry('POINT', srid=4326), nullable=False),
        sa.Column('address', sa.String(255), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('country_id', sa.Integer, sa.ForeignKey('countries.id'), nullable=True),
        sa.Column('region_id', sa.Integer, sa.ForeignKey('regions.id'), nullable=True),
        sa.Column('district_id', sa.Integer, sa.ForeignKey('districts.id'), nullable=True),
        sa.Column('ward_id', sa.Integer, sa.ForeignKey('wards.id'), nullable=True),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id'), nullable=True),
        sa.Column('thumbnail_url', sa.String(255), nullable=True),
        sa.Column('price_min', sa.Float, nullable=True),
        sa.Column('price_max', sa.Float, nullable=True),
        sa.Column('popularity_score', sa.Float, default=0.0),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )

    op.create_table(
        'location_amenities',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('location_id', sa.Integer, sa.ForeignKey('locations.id', ondelete='CASCADE')),
        sa.Column('name', sa.String(100))
    )

    op.create_table(
        'ratings',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('location_id', sa.Integer, sa.ForeignKey('locations.id', ondelete='CASCADE')),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('rating', sa.Float),
        sa.Column('comment', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now())
    )


def downgrade():
    op.drop_table('ratings')
    op.drop_table('location_amenities')
    op.drop_table('locations')
    op.drop_table('categories')
    op.drop_table('wards')
    op.drop_table('districts')
    op.drop_table('regions')
    op.drop_table('countries')
    op.drop_table('continents')
    op.drop_table('password_reset_tokens')
    op.drop_table('users')
