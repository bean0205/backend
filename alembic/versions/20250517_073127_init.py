# This script initializes alembic commands
# You can add custom commands here if needed

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '<revision_id>'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create table users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("email", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("is_superuser", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Create table password_reset_tokens
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("token", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("expires_at", sa.DateTime, nullable=False),
        sa.Column("is_used", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    # Create table countries
    op.create_table(
        "countries",
        sa.Column("id", sa.Integer, primary_key=True, index=True, comment="ID quốc gia"),
        sa.Column("code", sa.String(10), unique=True, index=True, nullable=False, comment="Mã quốc gia (VD: VN, US)"),
        sa.Column("name", sa.String(100), index=True, nullable=False, comment="Tên quốc gia"),
        comment="Quốc gia – ví dụ: Việt Nam, Mỹ, Nhật",
    )

    # Create table regions
    op.create_table(
        "regions",
        sa.Column("id", sa.Integer, primary_key=True, index=True, comment="ID vùng"),
        sa.Column("name", sa.String(100), index=True, nullable=False, comment="Tên vùng (VD: Hà Nội, California)"),
        sa.Column("country_id", sa.Integer, sa.ForeignKey("countries.id", ondelete="CASCADE"), nullable=False, comment="FK đến quốc gia"),
        comment="Vùng / tỉnh / thành phố – ví dụ: Hà Nội, Tokyo",
    )

    # Create table districts
    op.create_table(
        "districts",
        sa.Column("id", sa.Integer, primary_key=True, index=True, comment="ID quận/huyện"),
        sa.Column("name", sa.String(100), index=True, nullable=False, comment="Tên quận/huyện"),
        sa.Column("region_id", sa.Integer, sa.ForeignKey("regions.id", ondelete="CASCADE"), nullable=False, comment="FK đến vùng"),
        comment="Quận / huyện – ví dụ: Ba Đình, Quận 1",
    )

    # Create table wards
    op.create_table(
        "wards",
        sa.Column("id", sa.Integer, primary_key=True, index=True, comment="ID phường/xã"),
        sa.Column("name", sa.String(100), index=True, nullable=False, comment="Tên phường/xã"),
        sa.Column("district_id", sa.Integer, sa.ForeignKey("districts.id", ondelete="CASCADE"), nullable=False, comment="FK đến quận/huyện"),
        comment="Phường / xã – ví dụ: Phường Bến Nghé, Xã Tả Van",
    )

    # Create table categories
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer, primary_key=True, index=True, comment="ID loại địa điểm"),
        sa.Column("name", sa.String(100), unique=True, index=True, nullable=False, comment="Tên loại"),
        comment="Loại địa điểm – ví dụ: Cafe, Bảo tàng, Nhà hàng",
    )

    # Create table locations
    op.create_table(
        "locations",
        sa.Column("id", sa.Integer, primary_key=True, index=True, comment="ID địa điểm"),
        sa.Column("name", sa.String(255), index=True, nullable=False, comment="Tên địa điểm"),
        sa.Column("description", sa.Text, nullable=True, comment="Mô tả địa điểm"),
        sa.Column("latitude", sa.Float, nullable=False, comment="Vĩ độ (latitude)"),
        sa.Column("longitude", sa.Float, nullable=False, comment="Kinh độ (longitude)"),
        sa.Column("geom", Geometry("POINT", srid=4326), nullable=False, comment="Cột geometry kiểu POINT với SRID 4326 (WGS84)"),
        sa.Column("address", sa.String(255), nullable=True, comment="Địa chỉ chi tiết"),
        sa.Column("city", sa.String(100), nullable=True, comment="Tên thành phố (tự do nhập)"),
        sa.Column("country_id", sa.Integer, sa.ForeignKey("countries.id"), nullable=True, comment="FK quốc gia"),
        sa.Column("region_id", sa.Integer, sa.ForeignKey("regions.id"), nullable=True, comment="FK vùng"),
        sa.Column("district_id", sa.Integer, sa.ForeignKey("districts.id"), nullable=True, comment="FK quận/huyện"),
        sa.Column("ward_id", sa.Integer, sa.ForeignKey("wards.id"), nullable=True, comment="FK phường/xã"),
        sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id"), nullable=True, comment="FK loại địa điểm"),
        sa.Column("thumbnail_url", sa.String(255), nullable=True, comment="Ảnh đại diện (thumbnail)"),
        sa.Column("price_min", sa.Float, nullable=True, comment="Giá tối thiểu"),
        sa.Column("price_max", sa.Float, nullable=True, comment="Giá tối đa"),
        sa.Column("popularity_score", sa.Float, nullable=False, server_default="0.0", comment="Điểm phổ biến (dùng để sắp xếp)"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true"), comment="Cờ trạng thái hoạt động"),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now(), comment="Thời gian tạo"),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now(), comment="Thời gian cập nhật"),
        comment="Địa điểm cụ thể như quán cafe, điểm tham quan, nhà hàng...",
    )

    # Create table location_amenities
    op.create_table(
        "location_amenities",
        sa.Column("id", sa.Integer, primary_key=True, index=True, comment="ID tiện ích"),
        sa.Column("location_id", sa.Integer, sa.ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, comment="FK đến địa điểm"),
        sa.Column("name", sa.String(100), nullable=False, comment="Tên tiện ích (VD: Wifi, Máy lạnh)"),
        comment="Tiện ích của địa điểm – ví dụ: Wifi, điều hòa, bãi đỗ xe",
    )

    # Create table ratings
    op.create_table(
        "ratings",
        sa.Column("id", sa.Integer, primary_key=True, index=True, comment="ID đánh giá"),
        sa.Column("location_id", sa.Integer, sa.ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, comment="FK đến địa điểm"),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="FK đến người dùng"),
        sa.Column("rating", sa.Float, nullable=False, comment="Điểm đánh giá (1-5)"),
        sa.Column("comment", sa.Text, nullable=True, comment="Bình luận"),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now(), comment="Thời gian đánh giá"),
        comment="Đánh giá địa điểm bởi người dùng",
    )


def downgrade():
    op.drop_table("ratings")
    op.drop_table("location_amenities")
    op.drop_table("locations")
    op.drop_table("categories")
    op.drop_table("wards")
    op.drop_table("districts")
    op.drop_table("regions")
    op.drop_table("countries")
    op.drop_table("password_reset_tokens")
    op.drop_table("users")