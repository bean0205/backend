from datetime import datetime, timedelta
from typing import Optional, List, Any
import uuid

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Table, UniqueConstraint, \
    Date, Time, DECIMAL
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import func as sql_func
from geoalchemy2 import Geometry
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign, remote, backref

from app.db.session import Base

# Định nghĩa bảng liên kết giữa Role và Permission
role_permission = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True)
)


class Permission(AsyncAttrs, Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    code = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    roles = relationship("Role", secondary=role_permission, back_populates="permissions")


class Role(AsyncAttrs, Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    permissions = relationship("Permission", secondary=role_permission, back_populates="roles")
    users = relationship("User", back_populates="role")


class User(AsyncAttrs, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    role = relationship("Role", back_populates="users")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")
    accommodations = relationship("Accommodation", back_populates="user")
    ratings = relationship("Rating", back_populates="user")
    article_author = relationship("Article", back_populates="author")
    article_comments = relationship("ArticleComment", back_populates="user")
    article_reactions = relationship("ArticleReaction", back_populates="user")
    organizers = relationship("Organizer", back_populates="user")
    events = relationship("Event", back_populates="user")
    event_attendees = relationship("EventAttendee", back_populates="user")
    community_posts = relationship("CommunityPost", back_populates="user")
    community_post_comments = relationship("CommunityPostComment", back_populates="user")
    community_post_reactions = relationship("CommunityPostReaction", back_populates="user")


class PasswordResetToken(AsyncAttrs, Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="password_reset_tokens")


class Continent(AsyncAttrs, Base):
    __tablename__ = "continents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    name_code = Column(String(100))
    background_image = Column(String(255))
    logo = Column(String(255))
    description = Column(Text)
    description_code = Column(Text)
    status = Column(Integer, default=1, nullable=False)
    created_date = Column(Date, default=datetime.utcnow().date(), nullable=False)
    updated_date = Column(Date)

    # Relationships
    countries = relationship("Country", back_populates="continent")


class Country(AsyncAttrs, Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    name_code = Column(String(100))
    description = Column(Text)
    description_code = Column(Text)
    background_image = Column(String(255))
    logo = Column(String(255))
    status = Column(Integer, default=1, nullable=False)
    created_date = Column(Date, default=datetime.utcnow().date(), nullable=False)
    updated_date = Column(Date)
    continent_id = Column(Integer, ForeignKey("continents.id"), nullable=False, index=True)

    # Relationships
    continent = relationship("Continent", back_populates="countries")
    regions = relationship("Region", back_populates="country")
    locations = relationship("Location", back_populates="country")
    accommodations = relationship("Accommodation", back_populates="country")
    foods = relationship("Food", back_populates="country")
    articles = relationship("Article", back_populates="country")
    events = relationship("Event", back_populates="country")


class Region(AsyncAttrs, Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False)
    name_code = Column(String(100))
    description = Column(Text)
    description_code = Column(Text)
    background_image = Column(String(255))
    logo = Column(String(255))
    status = Column(Integer, default=1, nullable=False)
    created_date = Column(Date, default=datetime.utcnow().date(), nullable=False)
    updated_date = Column(Date)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False, index=True)

    # Relationships
    country = relationship("Country", back_populates="regions")
    districts = relationship("District", back_populates="region")
    locations = relationship("Location", back_populates="region")
    accommodations = relationship("Accommodation", back_populates="region")
    foods = relationship("Food", back_populates="region")
    articles = relationship("Article", back_populates="region")
    events = relationship("Event", back_populates="region")


class District(AsyncAttrs, Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False)
    name_code = Column(String(100))
    description = Column(Text)
    description_code = Column(Text)
    background_image = Column(String(255))
    logo = Column(String(255))
    status = Column(Integer, default=1, nullable=False)
    created_date = Column(Date, default=datetime.utcnow().date(), nullable=False)
    updated_date = Column(Date)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False, index=True)

    # Relationships
    region = relationship("Region", back_populates="districts")
    wards = relationship("Ward", back_populates="district")
    locations = relationship("Location", back_populates="district")
    accommodations = relationship("Accommodation", back_populates="district")
    foods = relationship("Food", back_populates="district")
    articles = relationship("Article", back_populates="district")
    events = relationship("Event", back_populates="district")


class Ward(AsyncAttrs, Base):
    __tablename__ = "wards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False)
    name_code = Column(String(100))
    description = Column(Text)
    description_code = Column(Text)
    background_image = Column(String(255))
    logo = Column(String(255))
    status = Column(Integer, default=1, nullable=False)
    created_date = Column(Date, default=datetime.utcnow().date(), nullable=False)
    updated_date = Column(Date)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False, index=True)

    # Relationships
    district = relationship("District", back_populates="wards")
    locations = relationship("Location", back_populates="ward")
    accommodations = relationship("Accommodation", back_populates="ward")
    foods = relationship("Food", back_populates="ward")
    articles = relationship("Article", back_populates="ward")
    events = relationship("Event", back_populates="ward")


class MediaType(AsyncAttrs, Base):
    __tablename__ = "media_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(Integer, default=1, nullable=False)
    created_date = Column(Date, default=datetime.utcnow().date(), nullable=False)
    updated_date = Column(Date)

    # Relationships
    media = relationship("Media", back_populates="type")


class MediaCategory(AsyncAttrs, Base):
    __tablename__ = "media_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(Integer, default=1, nullable=False)
    created_date = Column(Date, default=datetime.utcnow().date(), nullable=False)
    updated_date = Column(Date)

    # Relationships
    media = relationship("Media", back_populates="category")


class LocationCategory(AsyncAttrs, Base):
    __tablename__ = "location_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    locations = relationship("Location", back_populates="category")


class Location(AsyncAttrs, Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_code = Column(String(255))
    description = Column(Text)
    description_code = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    geom = Column(Text)  # Có thể sử dụng Geometry từ GeoAlchemy2 nếu cần
    address = Column(String(255))
    city = Column(String(100))
    country_id = Column(Integer, ForeignKey("countries.id"))
    region_id = Column(Integer, ForeignKey("regions.id"))
    district_id = Column(Integer, ForeignKey("districts.id"))
    ward_id = Column(Integer, ForeignKey("wards.id"))
    category_id = Column(Integer, ForeignKey("location_categories.id"), nullable=False)
    thumbnail_url = Column(String(255))
    price_min = Column(Float)
    price_max = Column(Float)
    popularity_score = Column(Float, default=0)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    country = relationship("Country", back_populates="locations")
    region = relationship("Region", back_populates="locations")
    district = relationship("District", back_populates="locations")
    ward = relationship("Ward", back_populates="locations")
    category = relationship("LocationCategory", back_populates="locations")
    ratings = relationship(
        "Rating",
        primaryjoin="and_(foreign(Rating.reference_id) == Location.id, Rating.reference_type == 'location')",
        back_populates="location"
    )
    media = relationship(
        "Media",
        primaryjoin="and_(foreign(Media.reference_id) == Location.id, Media.reference_type == 'location')",
        back_populates="location"
    )


class AccommodationCategory(AsyncAttrs, Base):
    __tablename__ = "accommodations_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    accommodations = relationship("Accommodation", back_populates="category")


class Accommodation(AsyncAttrs, Base):
    __tablename__ = "accommodations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    name_code = Column(String(255))
    description = Column(Text)
    description_code = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    geom = Column(Text)  # Có thể sử dụng Geometry từ GeoAlchemy2 nếu cần
    address = Column(String(255))
    city = Column(String(100))
    country_id = Column(Integer, ForeignKey("countries.id"))
    region_id = Column(Integer, ForeignKey("regions.id"))
    district_id = Column(Integer, ForeignKey("districts.id"))
    ward_id = Column(Integer, ForeignKey("wards.id"))
    category_id = Column(Integer, ForeignKey("accommodations_categories.id"), nullable=False)
    thumbnail_url = Column(String(255))
    price_min = Column(Float)
    price_max = Column(Float)
    popularity_score = Column(Float, default=0)
    checkin_time = Column(Time)
    checkout_time = Column(Time)
    cancel_policy = Column(Text)
    pet_policy = Column(Text)
    child_policy = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="accommodations")
    country = relationship("Country", back_populates="accommodations")
    region = relationship("Region", back_populates="accommodations")
    district = relationship("District", back_populates="accommodations")
    ward = relationship("Ward", back_populates="accommodations")
    category = relationship("AccommodationCategory", back_populates="accommodations")
    rooms = relationship("AccommodationRoom", back_populates="accommodation")
    media = relationship(
        "Media",
        primaryjoin="and_(foreign(Media.reference_id) == Accommodation.id, Media.reference_type == 'accommodation')",
        back_populates="accommodation"
    )
    ratings = relationship(
        "Rating",
        primaryjoin="and_(foreign(Rating.reference_id) == Accommodation.id, Rating.reference_type == 'accommodation')",
        back_populates="accommodation"
    )


class AccommodationRoom(AsyncAttrs, Base):
    __tablename__ = "accommodation_rooms"

    id = Column(Integer, primary_key=True, index=True)
    accommodation_id = Column(Integer, ForeignKey("accommodations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    name_code = Column(String(255))
    description = Column(Text)
    description_code = Column(Text)
    adult_capacity = Column(Integer, default=1, nullable=False)
    child_capacity = Column(Integer, default=0)
    room_area = Column(Integer)
    bed_capacity = Column(String(100))
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    accommodation = relationship("Accommodation", back_populates="rooms")


class Rating(AsyncAttrs, Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    reference_id = Column(Integer, nullable=False)
    reference_type = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="ratings")
    location = relationship("Location", foreign_keys=[reference_id],
                            primaryjoin="and_(Rating.reference_id == Location.id, Rating.reference_type == 'location')",
                            back_populates="ratings")
    accommodation = relationship("Accommodation", foreign_keys=[reference_id],
                                 primaryjoin="and_(Rating.reference_id == Accommodation.id, Rating.reference_type == 'accommodation')",
                                 back_populates="ratings")
    food = relationship("Food", foreign_keys=[reference_id],
                        primaryjoin="and_(foreign(Rating.reference_id) == Food.id, Rating.reference_type == 'food')",
                        back_populates="ratings")


class FoodCategory(AsyncAttrs, Base):
    __tablename__ = "food_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    foods = relationship("Food", back_populates="category")


class Food(AsyncAttrs, Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_code = Column(String(255))
    description = Column(Text)
    description_code = Column(Text)
    country_id = Column(Integer, ForeignKey("countries.id"))
    region_id = Column(Integer, ForeignKey("regions.id"))
    district_id = Column(Integer, ForeignKey("districts.id"))
    ward_id = Column(Integer, ForeignKey("wards.id"))
    category_id = Column(Integer, ForeignKey("food_categories.id"), nullable=False)
    thumbnail_url = Column(String(255))
    price_min = Column(Float)
    price_max = Column(Float)
    popularity_score = Column(Float, default=0)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    country = relationship("Country", back_populates="foods")
    region = relationship("Region", back_populates="foods")
    district = relationship("District", back_populates="foods")
    ward = relationship("Ward", back_populates="foods")
    category = relationship("FoodCategory", back_populates="foods")
    ratings = relationship(
        "Rating",
        primaryjoin="and_(foreign(Rating.reference_id) == Food.id, Rating.reference_type == 'food')",
        back_populates="food"
    )
    media = relationship(
        "Media",
        primaryjoin="and_(foreign(Media.reference_id) == Food.id, Media.reference_type == 'food')",
        back_populates="food"
    )


class ArticleCategory(AsyncAttrs, Base):
    __tablename__ = "article_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    articles = relationship("ArticleArticleCategory", back_populates="category")


class ArticleTag(AsyncAttrs, Base):
    __tablename__ = "article_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    name_code = Column(String(100))
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    articles = relationship("ArticleArticleTag", back_populates="tag")


class Article(AsyncAttrs, Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    title_code = Column(String(255))
    description = Column(Text)
    description_code = Column(Text)
    content = Column(Text, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"))
    region_id = Column(Integer, ForeignKey("regions.id"))
    district_id = Column(Integer, ForeignKey("districts.id"))
    ward_id = Column(Integer, ForeignKey("wards.id"))
    thumbnail_url = Column(String(255))
    view_count = Column(Integer, default=0)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    author = relationship("User", back_populates="article_author")
    country = relationship("Country", back_populates="articles")
    region = relationship("Region", back_populates="articles")
    district = relationship("District", back_populates="articles")
    ward = relationship("Ward", back_populates="articles")
    comments = relationship("ArticleComment", back_populates="article")
    reactions = relationship("ArticleReaction", back_populates="article")
    categories = relationship("ArticleArticleCategory", back_populates="article")
    tags = relationship("ArticleArticleTag", back_populates="article")
    media = relationship(
        "Media",
        primaryjoin="and_(foreign(Media.reference_id) == Article.id, Media.reference_type == 'article')",
        back_populates="article"
    )


class ArticleComment(AsyncAttrs, Base):
    __tablename__ = "article_comment"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="article_comments")
    article = relationship("Article", back_populates="comments")


class ArticleReaction(AsyncAttrs, Base):
    __tablename__ = "article_reaction"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="article_reactions")
    article = relationship("Article", back_populates="reactions")


class ArticleArticleCategory(AsyncAttrs, Base):
    __tablename__ = "article_article_categories"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)
    article_categories_id = Column(Integer, ForeignKey("article_categories.id"), nullable=False)

    # Relationships
    article = relationship("Article", back_populates="categories")
    category = relationship("ArticleCategory", back_populates="articles")


class ArticleArticleTag(AsyncAttrs, Base):
    __tablename__ = "article_article_tags"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)
    article_tags_id = Column(Integer, ForeignKey("article_tags.id"), nullable=False)

    # Relationships
    article = relationship("Article", back_populates="tags")
    tag = relationship("ArticleTag", back_populates="articles")


class Organizer(AsyncAttrs, Base):
    __tablename__ = "organizer"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    name_code = Column(String(255))
    description = Column(Text)
    description_code = Column(Text)
    email = Column(String(255))
    phone = Column(String(20))
    website = Column(String(255))
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="organizers")
    events = relationship("Event", back_populates="organizer")
    event_sponsors = relationship("EventSponsor", back_populates="organizer")
    media = relationship("Media",
                         primaryjoin="and_(foreign(Media.reference_id) == Organizer.id, Media.reference_type == 'organizer')",
                         back_populates="organizer")


class EventCategory(AsyncAttrs, Base):
    __tablename__ = "event_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    events = relationship("Event", back_populates="category")


class Event(AsyncAttrs, Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organizer_id = Column(Integer, ForeignKey("organizer.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("event_categories.id"), nullable=False)
    name = Column(String(255), nullable=False)
    name_code = Column(String(255))
    description = Column(Text)
    description_code = Column(Text)
    content = Column(Text)
    country_id = Column(Integer, ForeignKey("countries.id"))
    region_id = Column(Integer, ForeignKey("regions.id"))
    district_id = Column(Integer, ForeignKey("districts.id"))
    ward_id = Column(Integer, ForeignKey("wards.id"))
    thumbnail_url = Column(String(255))
    view_count = Column(Integer, default=0)
    start_time = Column(Time)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    price = Column(DECIMAL(10, 2))
    max_attendees = Column(Integer)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="events")
    organizer = relationship("Organizer", back_populates="events")
    category = relationship("EventCategory", back_populates="events")
    country = relationship("Country", back_populates="events")
    region = relationship("Region", back_populates="events")
    district = relationship("District", back_populates="events")
    ward = relationship("Ward", back_populates="events")
    attendees = relationship("EventAttendee", back_populates="event")
    sponsors = relationship("EventSponsor", back_populates="event")
    media = relationship("Media",
                         primaryjoin="and_(foreign(Media.reference_id) == Event.id, Media.reference_type == 'event')",
                         back_populates="event")


class EventAttendee(AsyncAttrs, Base):
    __tablename__ = "event_attendee"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="event_attendees")
    event = relationship("Event", back_populates="attendees")


class EventSponsor(AsyncAttrs, Base):
    __tablename__ = "event_sponsor"

    id = Column(Integer, primary_key=True, index=True)
    organizer_id = Column(Integer, ForeignKey("organizer.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    organizer = relationship("Organizer", back_populates="event_sponsors")
    event = relationship("Event", back_populates="sponsors")


class CommunityPostCategory(AsyncAttrs, Base):
    __tablename__ = "community_post_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    name_code = Column(String(100))
    description = Column(Text)
    description_code = Column(Text)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    posts = relationship("CommunityPost", back_populates="category")


class CommunityPostTag(AsyncAttrs, Base):
    __tablename__ = "community_post_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    posts = relationship("CommunityPostCommunityPostTag", back_populates="tag")


class CommunityPost(AsyncAttrs, Base):
    __tablename__ = "community_post"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("community_post_categories.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    thumbnail_url = Column(String(255))
    view_count = Column(Integer, default=0)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="community_posts")
    category = relationship("CommunityPostCategory", back_populates="posts")
    comments = relationship("CommunityPostComment", back_populates="post")
    reactions = relationship("CommunityPostReaction", back_populates="post")
    tags = relationship("CommunityPostCommunityPostTag", back_populates="post")
    media = relationship("Media",
                         primaryjoin="and_(foreign(Media.reference_id) == CommunityPost.id, Media.reference_type == 'community_post')",
                         back_populates="community_post")


class CommunityPostCommunityPostTag(AsyncAttrs, Base):
    __tablename__ = "community_post_community_post_tags"

    id = Column(Integer, primary_key=True, index=True)
    community_post_id = Column(Integer, ForeignKey("community_post.id"), nullable=False)
    community_post_tag_id = Column(Integer, ForeignKey("community_post_tags.id"), nullable=False)

    # Relationships
    post = relationship("CommunityPost", back_populates="tags")
    tag = relationship("CommunityPostTag", back_populates="posts")


class CommunityPostComment(AsyncAttrs, Base):
    __tablename__ = "community_post_comment"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("community_post.id"), nullable=False)
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey("community_post_comment.id"))
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="community_post_comments")
    post = relationship("CommunityPost", back_populates="comments")
    parent = relationship("CommunityPostComment", remote_side=[id], backref="replies")
    reactions = relationship("CommunityPostReaction",
                             primaryjoin="CommunityPostReaction.comment_id == CommunityPostComment.id",
                             back_populates="comment")


class CommunityPostReaction(AsyncAttrs, Base):
    __tablename__ = "community_post_reaction"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("community_post.id"), nullable=False)
    reaction_type = Column(String(20), nullable=False)
    comment_id = Column(Integer, ForeignKey("community_post_comment.id"))
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="community_post_reactions")
    post = relationship("CommunityPost", back_populates="reactions")
    comment = relationship("CommunityPostComment", foreign_keys=[comment_id], back_populates="reactions")


class Media(AsyncAttrs, Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("media_type.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("media_category.id"), nullable=False)
    reference_id = Column(Integer, nullable=False)
    reference_type = Column(String(50), nullable=False)
    url = Column(Text, nullable=False)
    title = Column(String(255))
    description = Column(Text)
    status = Column(Integer, default=1, nullable=False)
    created_date = Column(Date, default=datetime.utcnow().date(), nullable=False)
    updated_date = Column(Date)

    # Relationships
    type = relationship("MediaType", back_populates="media")
    category = relationship("MediaCategory", back_populates="media")
    location = relationship("Location", foreign_keys=[reference_id],
                            primaryjoin="and_(Media.reference_id == Location.id, Media.reference_type == 'location')",
                            back_populates="media")
    accommodation = relationship("Accommodation", foreign_keys=[reference_id],
                                 primaryjoin="and_(Media.reference_id == Accommodation.id, Media.reference_type == 'accommodation')",
                                 back_populates="media")
    food = relationship("Food", foreign_keys=[reference_id],
                        primaryjoin="and_(foreign(Media.reference_id) == Food.id, Media.reference_type == 'food')",
                        back_populates="media")
    article = relationship("Article", foreign_keys=[reference_id],
                           primaryjoin="and_(foreign(Media.reference_id) == Article.id, Media.reference_type == 'article')",
                           back_populates="media")
    organizer = relationship("Organizer", foreign_keys=[reference_id],
                             primaryjoin="and_(foreign(Media.reference_id) == Organizer.id, Media.reference_type == 'organizer')",
                             back_populates="media")
    event = relationship("Event", foreign_keys=[reference_id],
                         primaryjoin="and_(foreign(Media.reference_id) == Event.id, Media.reference_type == 'event')",
                         back_populates="media")
    community_post = relationship("CommunityPost", foreign_keys=[reference_id],
                                  primaryjoin="and_(Media.reference_id == CommunityPost.id, Media.reference_type == 'community_post')",
                                  back_populates="media")
