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
    __table_args__ = {"comment": "Quốc gia – ví dụ: Việt Nam, Mỹ, Nhật"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="ID quốc gia")
    code: Mapped[str] = mapped_column(String(10), unique=True, index=True, comment="Mã quốc gia (VD: VN, US)")
    name: Mapped[str] = mapped_column(String(100), index=True, comment="Tên quốc gia")

    regions: Mapped[List["Region"]] = relationship("Region", back_populates="country", cascade="all, delete-orphan")
    locations: Mapped[List["Location"]] = relationship("Location", back_populates="country", cascade="all, delete-orphan")


class Region(Base, AsyncAttrs):
    __tablename__ = "regions"
    __table_args__ = {"comment": "Vùng / tỉnh / thành phố – ví dụ: Hà Nội, Tokyo"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="ID vùng")
    name: Mapped[str] = mapped_column(String(100), index=True, comment="Tên vùng (VD: Hà Nội, California)")
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"), comment="FK đến quốc gia")

    country: Mapped[Country] = relationship("Country", back_populates="regions")
    districts: Mapped[List["District"]] = relationship("District", back_populates="region", cascade="all, delete-orphan")
    locations: Mapped[List["Location"]] = relationship("Location", back_populates="region")


class District(Base, AsyncAttrs):
    __tablename__ = "districts"
    __table_args__ = {"comment": "Quận / huyện – ví dụ: Ba Đình, Quận 1"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="ID quận/huyện")
    name: Mapped[str] = mapped_column(String(100), index=True, comment="Tên quận/huyện")
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id", ondelete="CASCADE"), comment="FK đến vùng")

    region: Mapped[Region] = relationship("Region", back_populates="districts")
    wards: Mapped[List["Ward"]] = relationship("Ward", back_populates="district", cascade="all, delete-orphan")
    locations: Mapped[List["Location"]] = relationship("Location", back_populates="district")


class Ward(Base, AsyncAttrs):
    __tablename__ = "wards"
    __table_args__ = {"comment": "Phường / xã – ví dụ: Phường Bến Nghé, Xã Tả Van"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="ID phường/xã")
    name: Mapped[str] = mapped_column(String(100), index=True, comment="Tên phường/xã")
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id", ondelete="CASCADE"), comment="FK đến quận/huyện")

    district: Mapped[District] = relationship("District", back_populates="wards")
    locations: Mapped[List["Location"]] = relationship("Location", back_populates="ward")


class Category(Base, AsyncAttrs):
    __tablename__ = "categories"
    __table_args__ = {"comment": "Loại địa điểm – ví dụ: Cafe, Bảo tàng, Nhà hàng"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="ID loại địa điểm")
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, comment="Tên loại")

    locations: Mapped[List["Location"]] = relationship("Location", back_populates="category")


class Location(Base, AsyncAttrs):
    __tablename__ = "locations"
    __table_args__ = {"comment": "Địa điểm cụ thể như quán cafe, điểm tham quan, nhà hàng..."}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="ID địa điểm")
    name: Mapped[str] = mapped_column(String(255), index=True, comment="Tên địa điểm")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="Mô tả địa điểm")

    latitude: Mapped[float] = mapped_column(Float, nullable=False, comment="Vĩ độ (latitude)")
    longitude: Mapped[float] = mapped_column(Float, nullable=False, comment="Kinh độ (longitude)")
    geom = Column(Geometry("POINT", srid=4326), nullable=False, comment="Cột geometry kiểu POINT với SRID 4326 (WGS84)")

    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Địa chỉ chi tiết")
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Tên thành phố (tự do nhập)")

    country_id: Mapped[Optional[int]] = mapped_column(ForeignKey("countries.id"), nullable=True, comment="FK quốc gia")
    region_id: Mapped[Optional[int]] = mapped_column(ForeignKey("regions.id"), nullable=True, comment="FK vùng")
    district_id: Mapped[Optional[int]] = mapped_column(ForeignKey("districts.id"), nullable=True, comment="FK quận/huyện")
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True, comment="FK phường/xã")
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True, comment="FK loại địa điểm")

    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Ảnh đại diện (thumbnail)")
    price_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Giá tối thiểu")
    price_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Giá tối đa")
    popularity_score: Mapped[float] = mapped_column(Float, default=0.0, comment="Điểm phổ biến (dùng để sắp xếp)")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="Cờ trạng thái hoạt động")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, comment="Thời gian tạo")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="Thời gian cập nhật")

    country: Mapped[Optional[Country]] = relationship("Country", back_populates="locations")
    region: Mapped[Optional[Region]] = relationship("Region", back_populates="locations")
    district: Mapped[Optional[District]] = relationship("District", back_populates="locations")
    ward: Mapped[Optional[Ward]] = relationship("Ward", back_populates="locations")
    category: Mapped[Optional[Category]] = relationship("Category", back_populates="locations")

    amenities_rel: Mapped[List["LocationAmenity"]] = relationship("LocationAmenity", back_populates="location", cascade="all, delete-orphan")
    ratings: Mapped[List["Rating"]] = relationship("Rating", back_populates="location", cascade="all, delete-orphan")

    @property
    def address_short(self) -> str:
        parts = []
        if self.ward:
            parts.append(self.ward.name)
        elif self.district:
            parts.append(self.district.name)
        elif self.region:
            parts.append(self.region.name)
        if self.country:
            parts.append(self.country.name)
        return ", ".join(parts)

    @property
    def average_rating(self) -> Optional[float]:
        if not self.ratings:
            return None
        return sum(r.rating for r in self.ratings) / len(self.ratings)


class LocationAmenity(Base, AsyncAttrs):
    __tablename__ = "location_amenities"
    __table_args__ = {"comment": "Tiện ích của địa điểm – ví dụ: Wifi, điều hòa, bãi đỗ xe"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="ID tiện ích")
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), comment="FK đến địa điểm")
    name: Mapped[str] = mapped_column(String(100), comment="Tên tiện ích (VD: Wifi, Máy lạnh)")

    location: Mapped["Location"] = relationship("Location", back_populates="amenities_rel")


class Rating(Base, AsyncAttrs):
    __tablename__ = "ratings"
    __table_args__ = {"comment": "Đánh giá địa điểm bởi người dùng"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="ID đánh giá")
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), comment="FK đến địa điểm")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), comment="FK đến người dùng")
    rating: Mapped[float] = mapped_column(Float, comment="Điểm đánh giá (1-5)")
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="Bình luận")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, comment="Thời gian đánh giá")

    location: Mapped["Location"] = relationship("Location", back_populates="ratings")