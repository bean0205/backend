# Tài liệu Hướng dẫn Phát triển
# William Travel Backend

## Mục lục
1. [Giới thiệu](#giới-thiệu)
2. [Cấu trúc dự án](#cấu-trúc-dự-án)
3. [Môi trường phát triển](#môi-trường-phát-triển)
4. [Quy trình phát triển API mới](#quy-trình-phát-triển-api-mới)
5. [Hướng dẫn chi tiết từng bước](#hướng-dẫn-chi-tiết-từng-bước)
6. [Các mẫu code](#các-mẫu-code)
7. [Kiểm thử](#kiểm-thử)
8. [Quy ước và thực hành tốt nhất](#quy-ước-và-thực-hành-tốt-nhất)
9. [Xử lý sự cố](#xử-lý-sự-cố)
10. [Tài liệu tham khảo](#tài-liệu-tham-khảo)

## Giới thiệu

Tài liệu này cung cấp hướng dẫn chi tiết để phát triển những API mới trong ứng dụng William Travel Backend. Ứng dụng được xây dựng dựa trên FastAPI, SQLAlchemy 2.x (async), và PostgreSQL với PostGIS cho hỗ trợ địa lý.

### Công nghệ chính

- **FastAPI**: Framework API hiệu suất cao với hỗ trợ async
- **SQLAlchemy 2.x**: ORM hiện đại với khả năng async
- **PostgreSQL + PostGIS**: Cơ sở dữ liệu quan hệ với hỗ trợ địa lý
- **Alembic**: Công cụ migration cho cơ sở dữ liệu
- **Pydantic v2**: Xác thực dữ liệu và quản lý cấu hình
- **Poetry**: Quản lý phụ thuộc và đóng gói ứng dụng

## Cấu trúc dự án

Cấu trúc dự án tuân theo mô hình phân lớp rõ ràng:

```
backend/
├── app/                      # Thư mục ứng dụng chính
│   ├── api/                  # API endpoints
│   │   ├── deps.py           # Dependency injection và xác thực
│   │   └── v1/               # API version 1
│   │       ├── endpoints/    # API endpoints theo resource
│   │       │   ├── auth.py   # Endpoints xác thực
│   │       │   ├── location.py  # Location endpoints
│   │       │   └── users.py  # User management endpoints
│   │       └── router.py     # API router tổng hợp
│   ├── core/                 # Core components
│   │   ├── config.py         # Configuration và settings
│   │   └── security.py       # JWT và password hashing
│   ├── crud/                 # CRUD operations theo model
│   │   ├── crud_location.py  # Location CRUD operations
│   │   └── crud_user.py      # User CRUD operations
│   ├── db/                   # Database modules
│   │   ├── models.py         # SQLAlchemy models
│   │   └── session.py        # Database session management
│   ├── schemas/              # Pydantic schemas cho request/response
│   │   ├── location.py       # Location schemas
│   │   └── user.py           # User schemas
│   ├── services/             # Business logic services
│   │   └── email_service.py  # Email services
│   ├── scripts/              # Scripts tiện ích
│   │   └── init_test_data.py # Tạo dữ liệu test
│   └── main.py               # FastAPI application
├── alembic/                  # Database migration
│   └── versions/             # Migration versions
├── tests/                    # Tests
│   ├── conftest.py           # Test fixtures
│   └── api/                  # API tests
│       └── v1/               # API v1 tests
├── docs/                     # Tài liệu
├── .env                      # Environment variables
├── alembic.ini               # Alembic configuration
├── pyproject.toml            # Poetry project definition
└── poetry.lock               # Poetry lock file
```

### Giải thích các thành phần

- **api/**: Chứa tất cả các endpoint API, được tổ chức theo phiên bản và tài nguyên
- **core/**: Các thành phần cốt lõi như cấu hình, bảo mật
- **crud/**: Các module chứa logic CRUD tách biệt cho từng model
- **db/**: Định nghĩa model SQLAlchemy và kết nối database
- **schemas/**: Định nghĩa Pydantic schema cho request/response
- **services/**: Các dịch vụ bổ sung như email, notification
- **scripts/**: Script tiện ích (tạo dữ liệu, seed DB)
- **tests/**: Unit test và integration test
- **alembic/**: Migration database

## Môi trường phát triển

### Yêu cầu

- Python 3.11+
- Docker và Docker Compose
- Poetry
- Git

### Thiết lập môi trường phát triển

1. **Clone dự án**:
   ```bash
   git clone <repository_url>
   cd william-travel/backend
   ```

2. **Cài đặt Poetry** (nếu chưa có):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Cài đặt dependencies**:
   ```bash
   poetry install
   ```

4. **Khởi chạy PostgreSQL với PostGIS qua Docker**:
   ```bash
   docker run --name postgres-postgis \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_DB=travel \
     -p 5432:5432 \
     -d postgis/postgis:14-3.3
   
   # Tạo extension PostGIS trong database
   docker exec -it postgres-postgis psql -U postgres -d travel -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   ```

5. **Tạo file `.env` trong thư mục gốc của dự án**:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/travel
   SECRET_KEY=your_development_secret_key
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. **Chạy migrations**:
   ```bash
   poetry run alembic upgrade head
   ```

7. **Tạo dữ liệu mẫu** (tùy chọn):
   ```bash
   poetry run python -m app.scripts.init_test_data
   ```

8. **Khởi động server phát triển**:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

## Quy trình phát triển API mới

Quy trình phát triển một API mới có tương tác với cơ sở dữ liệu bao gồm các bước sau:

1. **Phân tích yêu cầu**: Xác định cấu trúc dữ liệu và các API endpoint cần thiết
2. **Tạo SQLAlchemy Model**: Định nghĩa cấu trúc database
3. **Tạo Migration**: Cập nhật cơ sở dữ liệu với schema mới
4. **Tạo Pydantic Schema**: Định nghĩa schema cho request và response
5. **Tạo CRUD Functions**: Các hàm tương tác với database
6. **Tạo API Endpoint**: Triển khai endpoint với các phương thức HTTP
7. **Viết Unit Tests**: Đảm bảo đủ test coverage cho API mới
8. **Tạo dữ liệu mẫu**: (tùy chọn) Tạo script hoặc fixture dữ liệu mẫu

## Hướng dẫn chi tiết từng bước

Dưới đây là hướng dẫn chi tiết để tạo một API mới cho một tài nguyên "Tour" từ đầu đến cuối.

### Bước 1: Tạo SQLAlchemy Model

Mở file `app/db/models.py` và thêm model mới:

```python
class Tour(Base, AsyncAttrs):
    __tablename__ = "tours"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_days: Mapped[int] = mapped_column(Integer)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    max_participants: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Thông tin địa lý cho điểm khởi hành
    departure_location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("locations.id"), nullable=True
    )
    
    # Relationships
    departure_location: Mapped[Optional["Location"]] = relationship(back_populates="departure_tours")
    locations: Mapped[List["TourLocation"]] = relationship(back_populates="tour")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

# Bảng kết nối nhiều-nhiều giữa Tour và Location
class TourLocation(Base, AsyncAttrs):
    __tablename__ = "tour_locations"
    
    tour_id: Mapped[int] = mapped_column(ForeignKey("tours.id"), primary_key=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), primary_key=True)
    order: Mapped[int] = mapped_column(Integer)  # Thứ tự ghé thăm
    duration_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    tour: Mapped["Tour"] = relationship(back_populates="locations")
    location: Mapped["Location"] = relationship()

# Cập nhật model Location để hỗ trợ relationship mới
class Location(Base, AsyncAttrs):
    # ... existing code ...
    
    # Thêm relationship mới
    departure_tours: Mapped[List["Tour"]] = relationship(back_populates="departure_location")
```

### Bước 2: Tạo Migration với Alembic

```bash
poetry run alembic revision --autogenerate -m "add_tours_model"
poetry run alembic upgrade head
```

Kiểm tra file migration được tạo ra trong `alembic/versions/` và điều chỉnh nếu cần.

### Bước 3: Tạo Pydantic Schema

Tạo file `app/schemas/tour.py`:

```python
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional, Union

from pydantic import BaseModel, Field, validator

# Shared properties
class TourBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Tên tour")
    description: Optional[str] = Field(None, description="Mô tả chi tiết về tour")
    duration_days: int = Field(..., gt=0, description="Số ngày của tour")
    price: Decimal = Field(..., gt=0, description="Giá tour")
    start_date: Optional[date] = Field(None, description="Ngày bắt đầu tour")
    end_date: Optional[date] = Field(None, description="Ngày kết thúc tour")
    max_participants: int = Field(..., gt=0, description="Số người tối đa có thể tham gia tour")
    is_active: bool = Field(True, description="Trạng thái hoạt động của tour")
    departure_location_id: Optional[int] = Field(None, description="ID của địa điểm khởi hành")

# Properties to receive on creation
class TourCreate(TourBase):
    pass
    
    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if 'start_date' in values and v and values['start_date'] and v < values['start_date']:
            raise ValueError('Ngày kết thúc phải sau ngày bắt đầu')
        return v

# Properties to receive on update
class TourUpdate(TourBase):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_days: Optional[int] = None
    price: Optional[Decimal] = None
    max_participants: Optional[int] = None
    is_active: Optional[bool] = None
    departure_location_id: Optional[int] = None

# Properties shared by models returned from API
class TourInDBBase(TourBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Properties to return to client
class Tour(TourInDBBase):
    pass

# Tour with details of all associated locations
class TourWithLocations(Tour):
    locations: List["TourLocationDetail"] = []

# Tour Location Association
class TourLocationBase(BaseModel):
    location_id: int
    order: int
    duration_hours: Optional[int] = None
    notes: Optional[str] = None

class TourLocationCreate(TourLocationBase):
    pass

class TourLocationUpdate(TourLocationBase):
    location_id: Optional[int] = None
    order: Optional[int] = None

class TourLocationInDBBase(TourLocationBase):
    tour_id: int
    
    class Config:
        from_attributes = True

class TourLocation(TourLocationInDBBase):
    pass

class TourLocationDetail(TourLocation):
    location: "LocationSummary" = None

# Các class cho filtering và pagination
class TourFilterParams(BaseModel):
    page: int = Field(1, ge=1, description="Số trang, bắt đầu từ 1")
    size: int = Field(20, ge=1, le=100, description="Số lượng kết quả mỗi trang")
    search_term: Optional[str] = Field(None, description="Tìm kiếm theo tên tour")
    min_price: Optional[Decimal] = Field(None, description="Giá tối thiểu")
    max_price: Optional[Decimal] = Field(None, description="Giá tối đa")
    min_duration: Optional[int] = Field(None, description="Thời gian tối thiểu (ngày)")
    max_duration: Optional[int] = Field(None, description="Thời gian tối đa (ngày)")
    departure_location_id: Optional[int] = Field(None, description="Lọc theo địa điểm khởi hành")
    is_active: Optional[bool] = Field(None, description="Lọc theo trạng thái")
    
class PaginatedTourResponse(BaseModel):
    items: List[Tour]
    total: int
    page: int
    size: int
    pages: int

# Import để tránh circular import
from app.schemas.location import LocationSummary

# Update tour model để thêm LocationSummary
TourWithLocations.update_forward_refs()
TourLocationDetail.update_forward_refs()
```

### Bước 4: Tạo CRUD Functions

Tạo file `app/crud/crud_tour.py`:

```python
from datetime import date
from decimal import Decimal
from typing import List, Optional, Tuple, Any, Dict, Union

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.db.models import Tour, TourLocation, Location
from app.schemas.tour import TourCreate, TourUpdate, TourFilterParams, TourLocationCreate

class CRUDTour(CRUDBase[Tour, TourCreate, TourUpdate]):
    async def create_with_locations(
        self,
        db: AsyncSession,
        *,
        obj_in: TourCreate,
        locations: List[TourLocationCreate]
    ) -> Tour:
        """Tạo tour mới với danh sách địa điểm"""
        # Tạo tour trước
        tour = await self.create(db, obj_in=obj_in)
        
        # Thêm địa điểm vào tour
        if locations:
            tour_locations = []
            for loc_data in locations:
                tour_location = TourLocation(
                    tour_id=tour.id,
                    location_id=loc_data.location_id,
                    order=loc_data.order,
                    duration_hours=loc_data.duration_hours,
                    notes=loc_data.notes
                )
                tour_locations.append(tour_location)
            
            db.add_all(tour_locations)
            await db.flush()
            await db.refresh(tour)
        
        return tour
    
    async def get_with_locations(
        self,
        db: AsyncSession,
        *,
        id: int
    ) -> Optional[Tour]:
        """Lấy tour chi tiết cùng với các địa điểm liên quan"""
        query = (
            select(self.model)
            .options(
                selectinload(self.model.locations)
                .selectinload(TourLocation.location)
            )
            .options(
                selectinload(self.model.departure_location)
            )
            .where(self.model.id == id)
        )
        result = await db.execute(query)
        return result.scalars().first()
    
    async def update_locations(
        self,
        db: AsyncSession,
        *,
        tour: Tour,
        locations: List[TourLocationCreate]
    ) -> Tour:
        """Cập nhật danh sách địa điểm của tour"""
        # Xóa tất cả địa điểm hiện tại
        query = select(TourLocation).where(TourLocation.tour_id == tour.id)
        result = await db.execute(query)
        existing_locations = result.scalars().all()
        for loc in existing_locations:
            await db.delete(loc)
        
        # Thêm địa điểm mới
        if locations:
            tour_locations = []
            for loc_data in locations:
                tour_location = TourLocation(
                    tour_id=tour.id,
                    location_id=loc_data.location_id,
                    order=loc_data.order,
                    duration_hours=loc_data.duration_hours,
                    notes=loc_data.notes
                )
                tour_locations.append(tour_location)
            
            db.add_all(tour_locations)
        
        await db.flush()
        await db.refresh(tour)
        return tour
    
    async def get_multi_filter(
        self,
        db: AsyncSession,
        *,
        filter_params: TourFilterParams
    ) -> Tuple[List[Tour], int, int]:
        """Lấy danh sách tour với lọc và phân trang"""
        query = select(self.model)
        
        # Áp dụng các bộ lọc
        query = self._apply_filters(query, filter_params)
        
        # Đếm tổng số kết quả
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query) or 0
        
        # Tính số trang
        pages = (total + filter_params.size - 1) // filter_params.size
        
        # Thêm phân trang
        query = query.offset((filter_params.page - 1) * filter_params.size).limit(filter_params.size)
        
        # Thực thi truy vấn
        result = await db.execute(query)
        return result.scalars().all(), total, pages
    
    def _apply_filters(self, query, filter_params: TourFilterParams):
        """Áp dụng các bộ lọc cho truy vấn"""
        filters = []
        
        # Tìm kiếm theo tên
        if filter_params.search_term:
            filters.append(self.model.name.ilike(f"%{filter_params.search_term}%"))
        
        # Lọc theo giá
        if filter_params.min_price is not None:
            filters.append(self.model.price >= filter_params.min_price)
        if filter_params.max_price is not None:
            filters.append(self.model.price <= filter_params.max_price)
        
        # Lọc theo thời gian
        if filter_params.min_duration is not None:
            filters.append(self.model.duration_days >= filter_params.min_duration)
        if filter_params.max_duration is not None:
            filters.append(self.model.duration_days <= filter_params.max_duration)
        
        # Lọc theo địa điểm khởi hành
        if filter_params.departure_location_id is not None:
            filters.append(self.model.departure_location_id == filter_params.departure_location_id)
        
        # Lọc theo trạng thái
        if filter_params.is_active is not None:
            filters.append(self.model.is_active == filter_params.is_active)
        
        # Áp dụng tất cả các bộ lọc
        if filters:
            query = query.where(and_(*filters))
        
        # Sắp xếp mặc định theo created_at giảm dần (mới nhất trước)
        query = query.order_by(self.model.created_at.desc())
        
        return query

# Tạo instance của CRUDTour
tour = CRUDTour(Tour)
```

### Bước 5: Thêm CRUD instance vào `app/crud/__init__.py`

```python
from app.crud.crud_location import location
from app.crud.crud_tour import tour
from app.crud.crud_user import user

# Cho phép import trực tiếp từ module crud
__all__ = ["user", "location", "tour"]
```

### Bước 6: Tạo API Endpoint

Tạo file `app/api/v1/endpoints/tour.py`:

```python
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.schemas.tour import (
    Tour, TourCreate, TourUpdate, TourWithLocations,
    PaginatedTourResponse, TourFilterParams, TourLocationCreate
)

router = APIRouter()

@router.get("/", response_model=PaginatedTourResponse)
async def read_tours(
    db: AsyncSession = Depends(deps.get_db_session),
    page: int = Query(1, ge=1, description="Số trang, bắt đầu từ 1"),
    size: int = Query(20, ge=1, le=100, description="Số lượng kết quả mỗi trang"),
    search_term: Optional[str] = Query(None, description="Tìm kiếm theo tên tour"),
    min_price: Optional[float] = Query(None, description="Giá tối thiểu"),
    max_price: Optional[float] = Query(None, description="Giá tối đa"),
    min_duration: Optional[int] = Query(None, description="Thời gian tối thiểu (ngày)"),
    max_duration: Optional[int] = Query(None, description="Thời gian tối đa (ngày)"),
    departure_location_id: Optional[int] = Query(None, description="Lọc theo địa điểm khởi hành"),
    is_active: Optional[bool] = Query(None, description="Lọc theo trạng thái"),
) -> Any:
    """
    Lấy danh sách tour với các tùy chọn lọc và phân trang.
    """
    filter_params = TourFilterParams(
        page=page,
        size=size,
        search_term=search_term,
        min_price=min_price,
        max_price=max_price,
        min_duration=min_duration,
        max_duration=max_duration,
        departure_location_id=departure_location_id,
        is_active=is_active
    )
    
    tours, total, pages = await crud.tour.get_multi_filter(db, filter_params=filter_params)
    
    return {
        "items": tours,
        "total": total,
        "page": filter_params.page,
        "size": filter_params.size,
        "pages": pages
    }

@router.post("/", response_model=Tour, status_code=status.HTTP_201_CREATED)
async def create_tour(
    *,
    db: AsyncSession = Depends(deps.get_db_session),
    tour_in: TourCreate,
    locations: List[TourLocationCreate],
    current_user: schemas.User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Tạo tour mới (chỉ Admin).
    """
    tour = await crud.tour.create_with_locations(db, obj_in=tour_in, locations=locations)
    return tour

@router.get("/{tour_id}", response_model=TourWithLocations)
async def read_tour(
    *,
    db: AsyncSession = Depends(deps.get_db_session),
    tour_id: int,
) -> Any:
    """
    Lấy thông tin chi tiết của một tour cụ thể.
    """
    tour = await crud.tour.get_with_locations(db, id=tour_id)
    if not tour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour không tồn tại"
        )
    return tour

@router.put("/{tour_id}", response_model=Tour)
async def update_tour(
    *,
    db: AsyncSession = Depends(deps.get_db_session),
    tour_id: int,
    tour_in: TourUpdate,
    locations: Optional[List[TourLocationCreate]] = None,
    current_user: schemas.User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Cập nhật thông tin tour (chỉ Admin).
    """
    tour = await crud.tour.get(db, id=tour_id)
    if not tour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour không tồn tại"
        )
    
    tour = await crud.tour.update(db, db_obj=tour, obj_in=tour_in)
    
    # Cập nhật danh sách địa điểm nếu được cung cấp
    if locations is not None:
        tour = await crud.tour.update_locations(db, tour=tour, locations=locations)
    
    return tour

@router.delete("/{tour_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tour(
    *,
    db: AsyncSession = Depends(deps.get_db_session),
    tour_id: int,
    current_user: schemas.User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Xóa tour (chỉ Admin).
    """
    tour = await crud.tour.get(db, id=tour_id)
    if not tour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour không tồn tại"
        )
    
    await crud.tour.remove(db, id=tour_id)
```

### Bước 7: Cập nhật Router trong `app/api/v1/router.py`

```python
from fastapi import APIRouter

from app.api.v1.endpoints import auth, location, users, tour

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(location.router, prefix="/locations", tags=["locations"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tour.router, prefix="/tours", tags=["tours"])
```

### Bước 8: Viết Unit Test

Tạo file `tests/api/v1/test_tour.py`:

```python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.schemas.tour import TourCreate, TourLocationCreate
from app.tests.utils.tour import create_random_tour
from app.tests.utils.user import create_random_admin

pytestmark = pytest.mark.asyncio

async def test_create_tour(
    client: AsyncClient, db: AsyncSession, admin_token_headers: dict
) -> None:
    data = {
        "tour": {
            "name": "Test Tour",
            "description": "Test tour description",
            "duration_days": 5,
            "price": 1000.50,
            "max_participants": 15,
            "is_active": True
        },
        "locations": [
            {
                "location_id": 1,
                "order": 1,
                "duration_hours": 4,
                "notes": "Visit in the morning"
            },
            {
                "location_id": 2,
                "order": 2,
                "duration_hours": 3,
                "notes": "Visit in the afternoon"
            }
        ]
    }
    
    response = await client.post(
        f"{settings.API_V1_STR}/tours/",
        headers=admin_token_headers,
        json=data
    )
    
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == data["tour"]["name"]
    assert content["description"] == data["tour"]["description"]
    assert content["duration_days"] == data["tour"]["duration_days"]
    assert float(content["price"]) == data["tour"]["price"]
    assert "id" in content
    
    # Verify created in database
    tour_id = content["id"]
    tour = await crud.tour.get(db, id=tour_id)
    assert tour is not None
    assert tour.name == data["tour"]["name"]

async def test_read_tours(client: AsyncClient, db: AsyncSession) -> None:
    # Create a few tours first
    for i in range(3):
        await create_random_tour(db)
    
    response = await client.get(f"{settings.API_V1_STR}/tours/")
    assert response.status_code == 200
    
    content = response.json()
    assert "items" in content
    assert "total" in content
    assert "page" in content
    assert "size" in content
    assert "pages" in content
    assert content["total"] >= 3
    assert len(content["items"]) >= 3

async def test_read_tour(client: AsyncClient, db: AsyncSession) -> None:
    tour = await create_random_tour(db)
    
    response = await client.get(f"{settings.API_V1_STR}/tours/{tour.id}")
    assert response.status_code == 200
    
    content = response.json()
    assert content["id"] == tour.id
    assert content["name"] == tour.name
    assert "locations" in content

async def test_tour_not_found(client: AsyncClient) -> None:
    response = await client.get(f"{settings.API_V1_STR}/tours/9999")
    assert response.status_code == 404

async def test_update_tour(
    client: AsyncClient, db: AsyncSession, admin_token_headers: dict
) -> None:
    tour = await create_random_tour(db)
    
    data = {
        "tour": {
            "name": "Updated Tour Name",
            "price": 1200.75
        }
    }
    
    response = await client.put(
        f"{settings.API_V1_STR}/tours/{tour.id}",
        headers=admin_token_headers,
        json=data
    )
    
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["tour"]["name"]
    assert float(content["price"]) == data["tour"]["price"]
    
    # Check that other fields remain unchanged
    assert content["description"] == tour.description
    assert content["duration_days"] == tour.duration_days

async def test_delete_tour(
    client: AsyncClient, db: AsyncSession, admin_token_headers: dict
) -> None:
    tour = await create_random_tour(db)
    
    response = await client.delete(
        f"{settings.API_V1_STR}/tours/{tour.id}",
        headers=admin_token_headers
    )
    
    assert response.status_code == 204
    
    # Verify it's gone from database
    deleted_tour = await crud.tour.get(db, id=tour.id)
    assert deleted_tour is None
```

### Bước 9: Tạo Test Utils

Tạo file `tests/utils/tour.py`:

```python
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db.models import Tour, TourLocation
from app.schemas.tour import TourCreate, TourLocationCreate
from app.tests.utils.utils import random_lower_string

async def create_random_tour(
    db: AsyncSession,
    *,
    location_ids: Optional[List[int]] = None
) -> Tour:
    """Create a random tour for testing"""
    
    # Generate random data
    name = f"Tour {random_lower_string(8)}"
    description = f"Description for {name}"
    duration_days = random.randint(1, 14)
    price = Decimal(random.uniform(100, 5000)).quantize(Decimal("0.01"))
    max_participants = random.randint(5, 30)
    
    # Create start and end dates
    today = date.today()
    start_date = today + timedelta(days=random.randint(10, 30))
    end_date = start_date + timedelta(days=duration_days)
    
    tour_in = TourCreate(
        name=name,
        description=description,
        duration_days=duration_days,
        price=price,
        start_date=start_date,
        end_date=end_date,
        max_participants=max_participants,
        is_active=True,
    )
    
    # Create location associations if location IDs were provided
    locations = []
    if location_ids:
        for i, loc_id in enumerate(location_ids):
            locations.append(
                TourLocationCreate(
                    location_id=loc_id,
                    order=i+1,
                    duration_hours=random.randint(1, 8),
                    notes=f"Notes for location {loc_id}"
                )
            )
    
    tour = await crud.tour.create_with_locations(db, obj_in=tour_in, locations=locations)
    return tour
```

### Bước 10: Cập nhật `conftest.py` với fixtures mới

Thêm vào file `tests/conftest.py`:

```python
@pytest.fixture
async def admin_user(db: AsyncSession) -> User:
    """Return admin user for testing"""
    return await create_admin_user(db)

@pytest.fixture
async def admin_token_headers(client: AsyncClient, admin_user: User) -> Dict[str, str]:
    """Return admin token headers for testing"""
    return await get_user_token_headers(client=client, email=admin_user.email)
```

## Các mẫu code

### Mẫu SQLAlchemy Model

```python
class ModelName(Base, AsyncAttrs):
    __tablename__ = "table_name"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Foreign key
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("parents.id"), nullable=True)
    
    # Relationship
    parent: Mapped[Optional["Parent"]] = relationship(back_populates="children")
    children: Mapped[List["Child"]] = relationship(back_populates="parent")
    
    # PostGIS geography column
    location: Mapped[Optional[Geometry]] = mapped_column(
        Geometry(geometry_type='POINT', srid=4326), nullable=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
```

### Mẫu Pydantic Schema

```python
# Base schema
class ModelBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

# Create schema
class ModelCreate(ModelBase):
    parent_id: Optional[int] = None

# Update schema
class ModelUpdate(ModelBase):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    parent_id: Optional[int] = None

# DB schema
class ModelInDBBase(ModelBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Return schema
class Model(ModelInDBBase):
    pass

# Extended return schema
class ModelDetail(Model):
    children: List["ChildModel"] = []
```

### Mẫu CRUD

```python
class CRUDModel(CRUDBase[Model, ModelCreate, ModelUpdate]):
    async def get_with_relations(
        self,
        db: AsyncSession,
        *,
        id: int
    ) -> Optional[Model]:
        query = (
            select(self.model)
            .options(selectinload(self.model.relation))
            .where(self.model.id == id)
        )
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_multi_filter(
        self,
        db: AsyncSession,
        *,
        filter_params: FilterParams
    ) -> Tuple[List[Model], int, int]:
        # Base query
        query = select(self.model)
        
        # Apply filters
        if filter_params.search_term:
            query = query.where(self.model.name.ilike(f"%{filter_params.search_term}%"))
        
        if filter_params.is_active is not None:
            query = query.where(self.model.is_active == filter_params.is_active)
        
        # Add more filters as needed
        
        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query) or 0
        
        # Calculate pages
        pages = (total + filter_params.size - 1) // filter_params.size
        
        # Apply pagination
        query = query.offset((filter_params.page - 1) * filter_params.size).limit(filter_params.size)
        
        # Execute query
        result = await db.execute(query)
        return result.scalars().all(), total, pages

# Create instance
model = CRUDModel(Model)
```

### Mẫu API Endpoint

```python
@router.get("/", response_model=PaginatedResponse)
async def read_items(
    db: AsyncSession = Depends(deps.get_db_session),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search_term: Optional[str] = Query(None)
) -> Any:
    """
    Lấy danh sách các items với phân trang.
    """
    filter_params = FilterParams(
        page=page,
        size=size,
        search_term=search_term
    )
    
    items, total, pages = await crud.item.get_multi_filter(db, filter_params=filter_params)
    
    return {
        "items": items,
        "total": total,
        "page": filter_params.page,
        "size": filter_params.size,
        "pages": pages
    }

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    *,
    db: AsyncSession = Depends(deps.get_db_session),
    item_in: ItemCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Tạo item mới.
    """
    item = await crud.item.create(db, obj_in=item_in)
    return item

@router.get("/{item_id}", response_model=ItemDetail)
async def read_item(
    *,
    db: AsyncSession = Depends(deps.get_db_session),
    item_id: int
) -> Any:
    """
    Lấy thông tin chi tiết của một item.
    """
    item = await crud.item.get_with_relations(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item

@router.put("/{item_id}", response_model=Item)
async def update_item(
    *,
    db: AsyncSession = Depends(deps.get_db_session),
    item_id: int,
    item_in: ItemUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Cập nhật item.
    """
    item = await crud.item.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    item = await crud.item.update(db, db_obj=item, obj_in=item_in)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    *,
    db: AsyncSession = Depends(deps.get_db_session),
    item_id: int,
    current_user: User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Xóa item (chỉ admin).
    """
    item = await crud.item.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    await crud.item.remove(db, id=item_id)
```

## Kiểm thử

### Chạy Unit Tests

```bash
# Chạy tất cả tests
poetry run pytest

# Chạy tests với logs
poetry run pytest -v

# Chạy tests cho một module cụ thể
poetry run pytest tests/api/v1/test_tour.py -v

# Chạy với code coverage
poetry run pytest --cov=app --cov-report=term-missing
```

### Kiểm thử API bằng Swagger UI

1. Khởi động server phát triển:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

2. Truy cập Swagger UI:
   http://localhost:8000/docs

3. Thực hiện các API call trực tiếp từ giao diện Swagger UI

## Quy ước và thực hành tốt nhất

### Quy ước đặt tên

1. **File và thư mục**:
   - Tên file nên sử dụng snake_case: `tour_location.py`
   - Tên model/schema nên là số ít: `tour.py` không phải `tours.py`

2. **Classes**:
   - Tên class nên sử dụng PascalCase: `TourLocation`
   - Tên class nên là số ít: `Tour` không phải `Tours`

3. **Functions và variables**:
   - Tên hàm và biến nên sử dụng snake_case: `create_with_locations`
   - Hàm private nên có prefix dấu gạch dưới: `_apply_filters`

4. **Constants**:
   - Constants nên viết hoa và sử dụng snake_case: `MAX_TOUR_DURATION`

### Tổ chức code

1. **Phân chia trách nhiệm**:
   - API endpoints chỉ nên xử lý request/response và xác thực
   - Logic nghiệp vụ nên nằm trong CRUD hoặc services
   - Cơ sở dữ liệu nên tương tác qua CRUD, không trực tiếp từ endpoints

2. **Nguyên tắc thiết kế**:
   - Thiết kế theo nguyên tắc Single Responsibility Principle
   - Mỗi module nên có một trách nhiệm rõ ràng
   - Tách biệt model, schema, controller và service

3. **Type hinting**:
   - Luôn sử dụng type hints cho parameters và return types
   - Sử dụng Union và Optional khi cần thiết
   - Kiểm tra type với mypy

### Error handling

1. **HTTPException**:
   - Sử dụng FastAPI's HTTPException cho lỗi API
   - Cung cấp status_code và message rõ ràng

2. **Validation**:
   - Sử dụng Pydantic validators cho dữ liệu đầu vào
   - Kiểm tra tồn tại trước khi update/delete

3. **Các best practice**:
   - Xác thực người dùng qua Depends
   - Kiểm tra quyền truy cập trước khi thực hiện hành động

## Xử lý sự cố

### Database Migrations

**Vấn đề**: Migration thất bại

**Giải pháp**:
1. Kiểm tra log lỗi: `poetry run alembic upgrade head --sql`
2. Sửa lỗi trong file migration
3. Có thể cần tạo migration mới: `poetry run alembic revision --autogenerate -m "fix_previous_migration"`

### API Response Issues

**Vấn đề**: API trả về 500 Internal Server Error

**Giải pháp**:
1. Kiểm tra logs: `poetry run uvicorn app.main:app --reload --log-level debug`
2. Sử dụng try/except để bắt và xử lý exception

### Circular Imports

**Vấn đề**: Lỗi circular import

**Giải pháp**:
1. Sử dụng string annotation: `def get_user(user_id: int) -> "User":`
2. Sử dụng `update_forward_refs()` sau khi định nghĩa
3. Tổ chức cấu trúc dự án để tránh circular imports

## Tài liệu tham khảo

1. [FastAPI Documentation](https://fastapi.tiangolo.com/)
2. [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
3. [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
4. [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
5. [PostgreSQL Documentation](https://www.postgresql.org/docs/)
6. [PostGIS Documentation](https://postgis.net/documentation/)
7. [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
