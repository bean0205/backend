from datetime import datetime, timedelta
from typing import Optional, List
import uuid

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import func as sql_func
from geoalchemy2 import Geometry
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class User(Base, AsyncAttrs):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="user")  # "user" or "admin"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationship to password reset tokens
    password_reset_tokens: Mapped[List["PasswordResetToken"]] = relationship(
        "PasswordResetToken", back_populates="user", cascade="all, delete-orphan"
    )


class PasswordResetToken(Base, AsyncAttrs):
    __tablename__ = "password_reset_tokens"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship to user
    user: Mapped[User] = relationship("User", back_populates="password_reset_tokens")
    
    @classmethod
    def generate_token(cls, user_id: int, expiration_hours: int = 24) -> "PasswordResetToken":
        """Generate a new password reset token"""
        return cls(
            token=str(uuid.uuid4()),
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(hours=expiration_hours)
        )
    
    def is_valid(self) -> bool:
        """Check if token is valid (not used and not expired)"""
        return not self.is_used and datetime.utcnow() <= self.expires_at


class Country(Base, AsyncAttrs):
    __tablename__ = "countries"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    code: Mapped[str] = mapped_column(String(2), index=True)
    
    # Relationships
    regions: Mapped[List["Region"]] = relationship("Region", back_populates="country")
    locations: Mapped[List["Location"]] = relationship("Location", back_populates="country_rel")


class Region(Base, AsyncAttrs):
    __tablename__ = "regions"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    
    # Relationships
    country: Mapped[Country] = relationship("Country", back_populates="regions")
    locations: Mapped[List["Location"]] = relationship("Location", back_populates="region")


class Category(Base, AsyncAttrs):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    locations: Mapped[List["Location"]] = relationship("Location", back_populates="category")


class Amenity(Base, AsyncAttrs):
    __tablename__ = "amenities"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    icon: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Relationships
    location_amenities: Mapped[List["LocationAmenity"]] = relationship("LocationAmenity", back_populates="amenity")


class LocationAmenity(Base, AsyncAttrs):
    __tablename__ = "location_amenities"
    
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), primary_key=True)
    amenity_id: Mapped[int] = mapped_column(ForeignKey("amenities.id"), primary_key=True)
    
    # Relationships
    location: Mapped["Location"] = relationship("Location", back_populates="amenities_rel")
    amenity: Mapped[Amenity] = relationship("Amenity", back_populates="location_amenities")


class Rating(Base, AsyncAttrs):
    __tablename__ = "ratings"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    location: Mapped["Location"] = relationship("Location", back_populates="ratings")
    user: Mapped[User] = relationship("User")


class Location(Base, AsyncAttrs):
    __tablename__ = "locations"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    # PostGIS geometry column - POINT type with SRID 4326 (WGS84)
    geom = Column(Geometry("POINT", srid=4326), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Replace string country with relation
    country_id: Mapped[Optional[int]] = mapped_column(ForeignKey("countries.id"), nullable=True)
    region_id: Mapped[Optional[int]] = mapped_column(ForeignKey("regions.id"), nullable=True)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)
    
    # Additional fields
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    price_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    price_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    popularity_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    country_rel: Mapped[Optional[Country]] = relationship("Country", back_populates="locations")
    region: Mapped[Optional[Region]] = relationship("Region", back_populates="locations")
    category: Mapped[Optional[Category]] = relationship("Category", back_populates="locations")
    amenities_rel: Mapped[List[LocationAmenity]] = relationship("LocationAmenity", back_populates="location")
    ratings: Mapped[List[Rating]] = relationship("Rating", back_populates="location")
    
    @property
    def address_short(self) -> str:
        """Return a shortened address for display"""
        parts = []
        if self.city:
            parts.append(self.city)
        if self.country_rel and self.country_rel.name:
            parts.append(self.country_rel.name)
        return ", ".join(parts) if parts else self.address or ""
    
    @property
    def average_rating(self) -> Optional[float]:
        """Calculate average rating if ratings exist"""
        if not self.ratings:
            return None
        return sum(r.rating for r in self.ratings) / len(self.ratings)
