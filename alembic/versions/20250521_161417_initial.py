# This script initializes alembic commands
# You can add custom commands here if needed

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each role'),
        sa.Column('name', sa.String(50), unique=True, nullable=False, comment='Role name (e.g. Admin, Staff, User)'),
        sa.Column('description', sa.String(255), comment='Description of this role and its privileges'),
        sa.Column('is_default', sa.Boolean(), default=False, nullable=False, comment='Whether this is a default role'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when role was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when role was last updated'),
        comment='Stores user roles and their basic information'
    )

    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each permission'),
        sa.Column('name', sa.String(100), unique=True, nullable=False, comment='Permission name (e.g. Create User)'),
        sa.Column('description', sa.String(255), comment='Description of what this permission allows'),
        sa.Column('code', sa.String(100), unique=True, nullable=False,
                  comment='Permission code (e.g. user:create, article:delete)'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when permission was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when permission was last updated'),
        comment='Stores individual permissions that can be assigned to roles'
    )

    # Create role_permissions join table
    op.create_table(
        'role_permissions',
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), primary_key=True,
                  comment='Reference to the role'),
        sa.Column('permission_id', sa.Integer(), sa.ForeignKey('permissions.id'), primary_key=True,
                  comment='Reference to the permission'),
        comment='Maps which permissions are assigned to each role'
    )

    # Create users table - Now with role_id instead of role
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each user'),
        sa.Column('email', sa.String(255), unique=True, nullable=False, index=True,
                  comment='User email address, used as login username'),
        sa.Column('full_name', sa.String(255), nullable=False, comment='User full name'),
        sa.Column('hashed_password', sa.String(255), nullable=False, comment='Hashed password for security'),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), nullable=False,
                  comment='Reference to user role in roles table'),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False,
                  comment='Whether the user account is active'),
        sa.Column('is_superuser', sa.Boolean(), default=False, nullable=False,
                  comment='Whether the user has superuser privileges'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when user was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when user was last updated'),
        comment='Stores user account information'
    )

    # Create password_reset_tokens table
    op.create_table(
        'password_reset_tokens',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each token'),
        sa.Column('token', sa.String(255), unique=True, nullable=False, comment='Unique token for password reset'),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, comment='Reference to the user'),
        sa.Column('expires_at', sa.DateTime(), nullable=False, comment='Expiration timestamp for the token'),
        sa.Column('is_used', sa.Boolean(), default=False, nullable=False, comment='Whether the token has been used'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when token was created'),
        comment='Stores password reset tokens'
    )

    # Create continents table
    op.create_table(
        'continents',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each continent'),
        sa.Column('name', sa.String(100), nullable=False, comment='Continent name'),
        sa.Column('code', sa.String(10), unique=True, nullable=False, comment='Continent code (e.g. AS for Asia)'),
        sa.Column('name_code', sa.String(100), comment='Code for translation purposes'),
        sa.Column('background_image', sa.String(255), comment='Background image URL for continent'),
        sa.Column('logo', sa.String(255), comment='Logo URL for continent'),
        sa.Column('description', sa.Text(), comment='Description of the continent'),
        sa.Column('description_code', sa.Text(), comment='Description code for translation'),
        sa.Column('status', sa.Integer(), default=1, nullable=False, comment='Status: 1-active, 0-inactive'),
        sa.Column('created_date', sa.Date(), default=datetime.utcnow().date(), nullable=False,
                  comment='Date when record was created'),
        sa.Column('updated_date', sa.Date(), comment='Date when record was last updated'),
        comment='Stores continent information'
    )

    # Create countries table
    op.create_table(
        'countries',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each country'),
        sa.Column('code', sa.String(10), unique=True, nullable=False, comment='Country code (e.g. VN for Vietnam)'),
        sa.Column('name', sa.String(100), nullable=False, comment='Country name'),
        sa.Column('name_code', sa.String(100), comment='Code for translation purposes'),
        sa.Column('description', sa.Text(), comment='Description of the country'),
        sa.Column('description_code', sa.Text(), comment='Description code for translation'),
        sa.Column('background_image', sa.String(255), comment='Background image URL for country'),
        sa.Column('logo', sa.String(255), comment='Logo URL for country'),
        sa.Column('status', sa.Integer(), default=1, nullable=False, comment='Status: 1-active, 0-inactive'),
        sa.Column('created_date', sa.Date(), default=datetime.utcnow().date(), nullable=False,
                  comment='Date when record was created'),
        sa.Column('updated_date', sa.Date(), comment='Date when record was last updated'),
        sa.Column('continent_id', sa.Integer(), sa.ForeignKey('continents.id'), nullable=False, index=True,
                  comment='Reference to the continent'),
        comment='Stores country information'
    )

    # Create regions table
    op.create_table(
        'regions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each region'),
        sa.Column('name', sa.String(100), nullable=False, comment='Region name'),
        sa.Column('code', sa.String(20), nullable=False, comment='Region code'),
        sa.Column('name_code', sa.String(100), comment='Code for translation purposes'),
        sa.Column('description', sa.Text(), comment='Description of the region'),
        sa.Column('description_code', sa.Text(), comment='Description code for translation'),
        sa.Column('background_image', sa.String(255), comment='Background image URL for region'),
        sa.Column('logo', sa.String(255), comment='Logo URL for region'),
        sa.Column('status', sa.Integer(), default=1, nullable=False, comment='Status: 1-active, 0-inactive'),
        sa.Column('created_date', sa.Date(), default=datetime.utcnow().date(), nullable=False,
                  comment='Date when record was created'),
        sa.Column('updated_date', sa.Date(), comment='Date when record was last updated'),
        sa.Column('country_id', sa.Integer(), sa.ForeignKey('countries.id'), nullable=False, index=True,
                  comment='Reference to the country'),
        comment='Stores region information (provinces, states)'
    )

    # Create districts table
    op.create_table(
        'districts',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each district'),
        sa.Column('name', sa.String(100), nullable=False, comment='District name'),
        sa.Column('code', sa.String(20), nullable=False, comment='District code'),
        sa.Column('name_code', sa.String(100), comment='Code for translation purposes'),
        sa.Column('description', sa.Text(), comment='Description of the district'),
        sa.Column('description_code', sa.Text(), comment='Description code for translation'),
        sa.Column('background_image', sa.String(255), comment='Background image URL for district'),
        sa.Column('logo', sa.String(255), comment='Logo URL for district'),
        sa.Column('status', sa.Integer(), default=1, nullable=False, comment='Status: 1-active, 0-inactive'),
        sa.Column('created_date', sa.Date(), default=datetime.utcnow().date(), nullable=False,
                  comment='Date when record was created'),
        sa.Column('updated_date', sa.Date(), comment='Date when record was last updated'),
        sa.Column('region_id', sa.Integer(), sa.ForeignKey('regions.id'), nullable=False, index=True,
                  comment='Reference to the region'),
        comment='Stores district information (cities, counties)'
    )

    # Create wards table
    op.create_table(
        'wards',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each ward'),
        sa.Column('name', sa.String(100), nullable=False, comment='Ward name'),
        sa.Column('code', sa.String(20), nullable=False, comment='Ward code'),
        sa.Column('name_code', sa.String(100), comment='Code for translation purposes'),
        sa.Column('description', sa.Text(), comment='Description of the ward'),
        sa.Column('description_code', sa.Text(), comment='Description code for translation'),
        sa.Column('background_image', sa.String(255), comment='Background image URL for ward'),
        sa.Column('logo', sa.String(255), comment='Logo URL for ward'),
        sa.Column('status', sa.Integer(), default=1, nullable=False, comment='Status: 1-active, 0-inactive'),
        sa.Column('created_date', sa.Date(), default=datetime.utcnow().date(), nullable=False,
                  comment='Date when record was created'),
        sa.Column('updated_date', sa.Date(), comment='Date when record was last updated'),
        sa.Column('district_id', sa.Integer(), sa.ForeignKey('districts.id'), nullable=False, index=True,
                  comment='Reference to the district'),
        comment='Stores ward information (neighborhoods, localities)'
    )

    # Create media_type table
    op.create_table(
        'media_type',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each media type'),
        sa.Column('name', sa.String(100), nullable=False, comment='Media type name (e.g. Image, Video)'),
        sa.Column('description', sa.Text(), comment='Description of the media type'),
        sa.Column('status', sa.Integer(), default=1, nullable=False, comment='Status: 1-active, 0-inactive'),
        sa.Column('created_date', sa.Date(), default=datetime.utcnow().date(), nullable=False,
                  comment='Date when record was created'),
        sa.Column('updated_date', sa.Date(), comment='Date when record was last updated'),
        comment='Stores media file types (image, video, etc.)'
    )

    # Create media_category table
    op.create_table(
        'media_category',
        sa.Column('id', sa.Integer(), primary_key=True, index=True,
                  comment='Unique identifier for each media category'),
        sa.Column('name', sa.String(100), nullable=False, comment='Media category name'),
        sa.Column('description', sa.Text(), comment='Description of the media category'),
        sa.Column('status', sa.Integer(), default=1, nullable=False, comment='Status: 1-active, 0-inactive'),
        sa.Column('created_date', sa.Date(), default=datetime.utcnow().date(), nullable=False,
                  comment='Date when record was created'),
        sa.Column('updated_date', sa.Date(), comment='Date when record was last updated'),
        comment='Categorizes media files (profile images, location photos, etc.)'
    )

    # Create location_categories table
    op.create_table(
        'location_categories',
        sa.Column('id', sa.Integer(), primary_key=True, index=True,
                  comment='Unique identifier for each location category'),
        sa.Column('name', sa.String(100), nullable=False, comment='Category name (e.g. Beach, Mountain, Museum)'),
        sa.Column('status', sa.Boolean(), default=True, nullable=False, comment='Whether the category is active'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when category was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when category was last updated'),
        comment='Categorizes locations by type (attractions, natural sites, etc.)'
    )

    # Create locations table
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each location'),
        sa.Column('name', sa.String(255), nullable=False, comment='Location name'),
        sa.Column('name_code', sa.String(255), comment='Code for translation purposes'),
        sa.Column('description', sa.Text(), comment='Description of the location'),
        sa.Column('description_code', sa.Text(), comment='Description code for translation'),
        sa.Column('latitude', sa.Float(), comment='Latitude coordinate'),
        sa.Column('longitude', sa.Float(), comment='Longitude coordinate'),
        sa.Column('geom', sa.Text(), comment='Geometry data for spatial queries'),
        sa.Column('address', sa.String(255), comment='Street address'),
        sa.Column('city', sa.String(100), comment='City name'),
        sa.Column('country_id', sa.Integer(), sa.ForeignKey('countries.id'), comment='Reference to the country'),
        sa.Column('region_id', sa.Integer(), sa.ForeignKey('regions.id'), comment='Reference to the region'),
        sa.Column('district_id', sa.Integer(), sa.ForeignKey('districts.id'), comment='Reference to the district'),
        sa.Column('ward_id', sa.Integer(), sa.ForeignKey('wards.id'), comment='Reference to the ward'),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('location_categories.id'), nullable=False,
                  comment='Reference to the location category'),
        sa.Column('thumbnail_url', sa.String(255), comment='URL to the thumbnail image'),
        sa.Column('price_min', sa.Float(), comment='Minimum price for entry/activities'),
        sa.Column('price_max', sa.Float(), comment='Maximum price for entry/activities'),
        sa.Column('popularity_score', sa.Float(), default=0, comment='Popularity score for ranking'),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False, comment='Whether the location is active'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when location was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when location was last updated'),
        comment='Stores tourist attractions and places of interest'
    )

    # Create accommodations_categories table
    op.create_table(
        'accommodations_categories',
        sa.Column('id', sa.Integer(), primary_key=True, index=True,
                  comment='Unique identifier for each accommodation category'),
        sa.Column('name', sa.String(100), nullable=False, comment='Category name (e.g. Hotel, Hostel, Resort)'),
        sa.Column('status', sa.Boolean(), default=True, nullable=False, comment='Whether the category is active'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when category was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when category was last updated'),
        comment='Categorizes accommodations by type (hotels, hostels, resorts, etc.)'
    )

    # Create accommodations table
    op.create_table(
        'accommodations',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each accommodation'),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False,
                  comment='Reference to the user who manages this accommodation'),
        sa.Column('name', sa.String(255), nullable=False, comment='Accommodation name'),
        sa.Column('name_code', sa.String(255), comment='Code for translation purposes'),
        sa.Column('description', sa.Text(), comment='Description of the accommodation'),
        sa.Column('description_code', sa.Text(), comment='Description code for translation'),
        sa.Column('latitude', sa.Float(), comment='Latitude coordinate'),
        sa.Column('longitude', sa.Float(), comment='Longitude coordinate'),
        sa.Column('geom', sa.Text(), comment='Geometry data for spatial queries'),
        sa.Column('address', sa.String(255), comment='Street address'),
        sa.Column('city', sa.String(100), comment='City name'),
        sa.Column('country_id', sa.Integer(), sa.ForeignKey('countries.id'), comment='Reference to the country'),
        sa.Column('region_id', sa.Integer(), sa.ForeignKey('regions.id'), comment='Reference to the region'),
        sa.Column('district_id', sa.Integer(), sa.ForeignKey('districts.id'), comment='Reference to the district'),
        sa.Column('ward_id', sa.Integer(), sa.ForeignKey('wards.id'), comment='Reference to the ward'),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('accommodations_categories.id'), nullable=False,
                  comment='Reference to the accommodation category'),
        sa.Column('thumbnail_url', sa.String(255), comment='URL to the thumbnail image'),
        sa.Column('price_min', sa.Float(), comment='Minimum price per night'),
        sa.Column('price_max', sa.Float(), comment='Maximum price per night'),
        sa.Column('popularity_score', sa.Float(), default=0, comment='Popularity score for ranking'),
        sa.Column('checkin_time', sa.Time(), comment='Standard check-in time'),
        sa.Column('checkout_time', sa.Time(), comment='Standard check-out time'),
        sa.Column('cancel_policy', sa.Text(), comment='Cancellation policy description'),
        sa.Column('pet_policy', sa.Text(), comment='Pet policy description'),
        sa.Column('child_policy', sa.Text(), comment='Child policy description'),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False,
                  comment='Whether the accommodation is active'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when accommodation was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when accommodation was last updated'),
        comment='Stores accommodation information (hotels, hostels, resorts, etc.)'
    )

    # Create accommodation_rooms table
    op.create_table(
        'accommodation_rooms',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each room'),
        sa.Column('accommodation_id', sa.Integer(), sa.ForeignKey('accommodations.id'), nullable=False,
                  comment='Reference to the accommodation'),
        sa.Column('name', sa.String(255), nullable=False, comment='Room name or number'),
        sa.Column('name_code', sa.String(255), comment='Code for translation purposes'),
        sa.Column('description', sa.Text(), comment='Description of the room'),
        sa.Column('description_code', sa.Text(), comment='Description code for translation'),
        sa.Column('adult_capacity', sa.Integer(), default=1, nullable=False, comment='Maximum number of adults'),
        sa.Column('child_capacity', sa.Integer(), default=0, comment='Maximum number of children'),
        sa.Column('room_area', sa.Integer(), comment='Room area in square meters'),
        sa.Column('bed_capacity', sa.String(100), comment='Description of bed configuration'),
        sa.Column('status', sa.Integer(), default=1, nullable=False, comment='Status: 1-active, 0-inactive'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when room was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when room was last updated'),
        comment='Stores individual rooms within accommodations'
    )

    # Create ratings table
    op.create_table(
        'ratings',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each rating'),
        sa.Column('reference_id', sa.Integer(), nullable=False, comment='ID of the item being rated'),
        sa.Column('reference_type', sa.String(50), nullable=False,
                  comment='Type of item being rated (location, accommodation, food, etc.)'),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False,
                  comment='Reference to the user who created the rating'),
        sa.Column('rating', sa.Float(), nullable=False, comment='Rating value (usually 1-5)'),
        sa.Column('comment', sa.Text(), comment='Review comment'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when rating was created'),
        comment='Stores user ratings and reviews for different entities'
    )

    # Create food_categories table
    op.create_table(
        'food_categories',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each food category'),
        sa.Column('name', sa.String(100), nullable=False, comment='Category name (e.g. Restaurant, Street Food, Cafe)'),
        sa.Column('status', sa.Boolean(), default=True, nullable=False, comment='Whether the category is active'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when category was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when category was last updated'),
        comment='Categorizes food establishments and cuisine types'
    )

    # Create food table
    op.create_table(
        'food',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each food entry'),
        sa.Column('name', sa.String(255), nullable=False, comment='Name of the food establishment or dish'),
        sa.Column('name_code', sa.String(255), comment='Code for translation purposes'),
        sa.Column('description', sa.Text(), comment='Description of the food or establishment'),
        sa.Column('description_code', sa.Text(), comment='Description code for translation'),
        sa.Column('country_id', sa.Integer(), sa.ForeignKey('countries.id'), comment='Reference to the country'),
        sa.Column('region_id', sa.Integer(), sa.ForeignKey('regions.id'), comment='Reference to the region'),
        sa.Column('district_id', sa.Integer(), sa.ForeignKey('districts.id'), comment='Reference to the district'),
        sa.Column('ward_id', sa.Integer(), sa.ForeignKey('wards.id'), comment='Reference to the ward'),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('food_categories.id'), nullable=False,
                  comment='Reference to the food category'),
        sa.Column('thumbnail_url', sa.String(255), comment='URL to the thumbnail image'),
        sa.Column('price_min', sa.Float(), comment='Minimum price range'),
        sa.Column('price_max', sa.Float(), comment='Maximum price range'),
        sa.Column('popularity_score', sa.Float(), default=0, comment='Popularity score for ranking'),
        sa.Column('status', sa.Boolean(), default=True, nullable=False, comment='Whether this food entry is active'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when entry was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when entry was last updated'),
        comment='Stores information about restaurants, food vendors and dishes'
    )

    # Create article_categories table
    op.create_table(
        'article_categories',
        sa.Column('id', sa.Integer(), primary_key=True, index=True,
                  comment='Unique identifier for each article category'),
        sa.Column('name', sa.String(100), nullable=False, comment='Category name (e.g. Travel Guide, Food Review)'),
        sa.Column('status', sa.Boolean(), default=True, nullable=False, comment='Whether the category is active'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when category was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when category was last updated'),
        comment='Categorizes articles by their type or subject'
    )

    # Create article_tags table
    op.create_table(
        'article_tags',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each article tag'),
        sa.Column('name', sa.String(100), nullable=False, comment='Tag name (e.g. Vietnam, Budget Travel, Adventure)'),
        sa.Column('name_code', sa.String(100), comment='Code for translation purposes'),
        sa.Column('status', sa.Boolean(), default=True, nullable=False, comment='Whether the tag is active'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when tag was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow, comment='Timestamp when tag was last updated'),
        comment='Tags for organizing and finding articles'
    )

    # Create article table
    op.create_table(
        'article',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each article'),
        sa.Column('author_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False,
                  comment='Reference to the article author'),
        sa.Column('title', sa.String(255), nullable=False, comment='Article title'),
        sa.Column('title_code', sa.String(255), comment='Code for translation purposes'),
        sa.Column('description', sa.Text(), comment='Short description or summary of the article'),
        sa.Column('description_code', sa.Text(), comment='Description code for translation'),
        sa.Column('content', sa.Text(), nullable=False, comment='Full article content (markdown or HTML)'),
        sa.Column('country_id', sa.Integer(), sa.ForeignKey('countries.id'),
                  comment='Reference to the country this article is about'),
        sa.Column('region_id', sa.Integer(), sa.ForeignKey('regions.id'),
                  comment='Reference to the region this article is about'),
        sa.Column('district_id', sa.Integer(), sa.ForeignKey('districts.id'),
                  comment='Reference to the district this article is about'),
        sa.Column('ward_id', sa.Integer(), sa.ForeignKey('wards.id'),
                  comment='Reference to the ward this article is about'),
        sa.Column('thumbnail_url', sa.String(255), comment='URL to the thumbnail image'),
        sa.Column('view_count', sa.Integer(), default=0, comment='Number of times the article has been viewed'),
        sa.Column('status', sa.Boolean(), default=True, nullable=False,
                  comment='Whether the article is published/active'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when article was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when article was last updated'),
        comment='Stores travel guides, blog posts, and other written content'
    )

    # Create article_comment table
    op.create_table(
        'article_comment',
        sa.Column('id', sa.Integer(), primary_key=True, index=True,
                  comment='Unique identifier for each article comment'),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False,
                  comment='Reference to the user who created the comment'),
        sa.Column('article_id', sa.Integer(), sa.ForeignKey('article.id'), nullable=False,
                  comment='Reference to the article being commented on'),
        sa.Column('content', sa.Text(), nullable=False, comment='Comment text content'),
        sa.Column('status', sa.Boolean(), default=True, nullable=False,
                  comment='Whether the comment is active/visible'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when comment was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when comment was last updated'),
        comment='Stores user comments on articles'
    )

    # Create article_reaction table
    op.create_table(
        'article_reaction',
        sa.Column('id', sa.Integer(), primary_key=True, index=True,
                  comment='Unique identifier for each article reaction'),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False,
                  comment='Reference to the user who reacted'),
        sa.Column('article_id', sa.Integer(), sa.ForeignKey('article.id'), nullable=False,
                  comment='Reference to the article being reacted to'),
        sa.Column('status', sa.Boolean(), default=True, nullable=False,
                  comment='Whether the reaction is active (like/unlike status)'),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False,
                  comment='Timestamp when reaction was created'),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow,
                  comment='Timestamp when reaction was last updated'),
        comment='Stores user reactions (likes) on articles'
    )

    # Create article_article_categories table
    op.create_table(
        'article_article_categories',
        sa.Column('id', sa.Integer(), primary_key=True, index=True,
                  comment='Unique identifier for each article-category relationship'),
        sa.Column('article_id', sa.Integer(), sa.ForeignKey('article.id'), nullable=False,
                  comment='Reference to the article'),
        sa.Column('article_categories_id', sa.Integer(), sa.ForeignKey('article_categories.id'), nullable=False,
                  comment='Reference to the article category'),
        comment='Junction table linking articles to their categories'
    )

    # Create article_article_tags table
    op.create_table(
        'article_article_tags',
        sa.Column('id', sa.Integer(), primary_key=True, index=True,
                  comment='Unique identifier for each article-tag relationship'),
        sa.Column('article_id', sa.Integer(), sa.ForeignKey('article.id'), nullable=False,
                  comment='Reference to the article'),
        sa.Column('article_tags_id', sa.Integer(), sa.ForeignKey('article_tags.id'), nullable=False,
                  comment='Reference to the article tag'),
        comment='Junction table linking articles to their tags'
    )

    # Create organizer table
    op.create_table(
        'organizer',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('name_code', sa.String(255)),
        sa.Column('description', sa.Text()),
        sa.Column('description_code', sa.Text()),
        sa.Column('email', sa.String(255)),
        sa.Column('phone', sa.String(20)),
        sa.Column('website', sa.String(255)),
        sa.Column('status', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow)
    )

    # Create event_categories table
    op.create_table(
        'event_categories',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('status', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow)
    )

    # Create event table
    op.create_table(
        'event',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('organizer_id', sa.Integer(), sa.ForeignKey('organizer.id'), nullable=False),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('event_categories.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('name_code', sa.String(255)),
        sa.Column('description', sa.Text()),
        sa.Column('description_code', sa.Text()),
        sa.Column('content', sa.Text()),
        sa.Column('country_id', sa.Integer(), sa.ForeignKey('countries.id')),
        sa.Column('region_id', sa.Integer(), sa.ForeignKey('regions.id')),
        sa.Column('district_id', sa.Integer(), sa.ForeignKey('districts.id')),
        sa.Column('ward_id', sa.Integer(), sa.ForeignKey('wards.id')),
        sa.Column('thumbnail_url', sa.String(255)),
        sa.Column('view_count', sa.Integer(), default=0),
        sa.Column('start_time', sa.Time()),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date()),
        sa.Column('price', sa.DECIMAL(10, 2)),
        sa.Column('max_attendees', sa.Integer()),
        sa.Column('status', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow)
    )

    # Create event_attendee table
    op.create_table(
        'event_attendee',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('event_id', sa.Integer(), sa.ForeignKey('event.id'), nullable=False),
        sa.Column('status', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow)
    )

    # Create event_sponsor table
    op.create_table(
        'event_sponsor',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('organizer_id', sa.Integer(), sa.ForeignKey('organizer.id'), nullable=False),
        sa.Column('event_id', sa.Integer(), sa.ForeignKey('event.id'), nullable=False),
        sa.Column('status', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow)
    )

    # Create community_post_categories table
    op.create_table(
        'community_post_categories',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('name_code', sa.String(100)),
        sa.Column('description', sa.Text()),
        sa.Column('description_code', sa.Text()),
        sa.Column('status', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow)
    )

    # Create community_post_tags table
    op.create_table(
        'community_post_tags',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('status', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow)
    )

    # Create community_post table
    op.create_table(
        'community_post',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('community_post_categories.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('thumbnail_url', sa.String(255)),
        sa.Column('view_count', sa.Integer(), default=0),
        sa.Column('status', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow)
    )

    # Create community_post_community_post_tags table
    op.create_table(
        'community_post_community_post_tags',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('community_post_id', sa.Integer(), sa.ForeignKey('community_post.id'), nullable=False),
        sa.Column('community_post_tag_id', sa.Integer(), sa.ForeignKey('community_post_tags.id'), nullable=False)
    )

    # Create community_post_comment table
    op.create_table(
        'community_post_comment',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey('community_post.id'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('community_post_comment.id')),
        sa.Column('status', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow)
    )

    # Create community_post_reaction table
    op.create_table(
        'community_post_reaction',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey('community_post.id'), nullable=False),
        sa.Column('reaction_type', sa.String(20), nullable=False),
        sa.Column('comment_id', sa.Integer(), sa.ForeignKey('community_post_comment.id')),
        sa.Column('status', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.utcnow)
    )

    # Create media table
    op.create_table(
        'media',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, comment='Unique identifier for each media file'),
        sa.Column('type_id', sa.Integer(), sa.ForeignKey('media_type.id'), nullable=False,
                  comment='Reference to media type (image, video, etc.)'),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('media_category.id'), nullable=False,
                  comment='Reference to media category (profile photo, location image, etc.)'),
        sa.Column('reference_id', sa.Integer(), nullable=False,
                  comment='ID of the entity this media belongs to (accommodation, food, location, etc.)'),
        sa.Column('reference_type', sa.String(50), nullable=False,
                  comment='Type of entity this media belongs to (accommodation, food, location, etc.)'),
        sa.Column('url', sa.Text(), nullable=False, comment='URL to access the media file'),
        sa.Column('title', sa.String(255), comment='Optional title for the media'),
        sa.Column('description', sa.Text(), comment='Optional description of the media content'),
        sa.Column('status', sa.Integer(), default=1, nullable=False, comment='Status: 1-active, 0-inactive'),
        sa.Column('created_date', sa.Date(), default=datetime.utcnow().date(), nullable=False,
                  comment='Date when media was added'),
        sa.Column('updated_date', sa.Date(), comment='Date when media was last updated'),
        comment='Stores information about media files (images, videos, documents) related to other entities'
    )

    # Create indexes with existence checks
    op.execute("CREATE INDEX IF NOT EXISTS ix_users_email ON users (email)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_continents_code ON continents (code)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_countries_code ON countries (code)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_countries_continent_id ON countries (continent_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_regions_country_id ON regions (country_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_districts_region_id ON districts (region_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_wards_district_id ON wards (district_id)")


def downgrade():
    # Drop tables in reverse order to respect foreign key constraints
    op.drop_table('media')
    op.drop_table('community_post_reaction')
    op.drop_table('community_post_comment')
    op.drop_table('community_post_community_post_tags')
    op.drop_table('community_post')
    op.drop_table('community_post_tags')
    op.drop_table('community_post_categories')
    op.drop_table('event_sponsor')
    op.drop_table('event_attendee')
    op.drop_table('event')
    op.drop_table('event_categories')
    op.drop_table('organizer')
    op.drop_table('article_article_tags')
    op.drop_table('article_article_categories')
    op.drop_table('article_reaction')
    op.drop_table('article_comment')
    op.drop_table('article')
    op.drop_table('article_tags')
    op.drop_table('article_categories')
    op.drop_table('food')
    op.drop_table('food_categories')
    op.drop_table('ratings')
    op.drop_table('accommodation_rooms')
    op.drop_table('accommodations')
    op.drop_table('accommodations_categories')
    op.drop_table('locations')
    op.drop_table('location_categories')
    op.drop_table('media_category')
    op.drop_table('media_type')
    op.drop_table('wards')
    op.drop_table('districts')
    op.drop_table('regions')
    op.drop_table('countries')
    op.drop_table('continents')
    op.drop_table('password_reset_tokens')
    op.drop_table('users')
    op.drop_table('role_permissions')
    op.drop_table('permissions')
    op.drop_table('roles')
    # Drop spatial_ref_sys table if it exists
