# William Travel Backend

Backend API cho ứng dụng William Travel được xây dựng với FastAPI, SQLAlchemy 2.x (async), và PostgreSQL với PostGIS để hỗ trợ xử lý dữ liệu địa lý.

![Python](https://img.shields.io/badge/python-v3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0+-00a393.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.21+-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-latest-blue.svg)
![PostGIS](https://img.shields.io/badge/PostGIS-latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Tính năng

- **FastAPI framework** với hỗ trợ async cho phát triển API hiệu suất cao
- **SQLAlchemy 2.x ORM** với khả năng async cho tương tác cơ sở dữ liệu hiện đại
- **PostgreSQL** với extension **PostGIS** cho các thao tác dữ liệu địa lý mạnh mẽ
- **Alembic** cho quản lý và thực thi database migrations
- **JWT Authentication** cho xác thực người dùng an toàn
- **Role-based Authorization** (Admin/User) để phân quyền truy cập tài nguyên
- **Advanced filtering & Pagination** cho API Location với nhiều tiêu chí lọc
- **Pydantic v2** cho việc xác thực dữ liệu và quản lý cấu hình
- **Poetry** để quản lý dependency và packaging
- **Tài liệu API tự động** với Swagger UI và ReDoc
- **Kiến trúc Async-first** xuyên suốt ứng dụng
- **ASGI server**: Uvicorn (dev), Gunicorn + Uvicorn (prod)
- **Type hints** trong toàn bộ mã nguồn để hỗ trợ IDE tốt hơn và nâng cao chất lượng code

## Cấu trúc dự án

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
│   │   └── email_service.py  # Email services cho reset password
│   ├── scripts/              # Scripts tiện ích
│   │   ├── init_test_data.py # Khởi tạo dữ liệu test
│   │   └── setup_database.py # Thiết lập cơ sở dữ liệu
│   └── main.py               # FastAPI application
├── alembic/                  # Database migration
│   └── versions/             # Migration versions
│       ├── 001_initial.py    # Initial migration
│       ├── 002_user_auth.py  # Auth migration
│       ├── 003_user_roles.py # Roles migration
│       └── 004_location_filtering.py # Location filter migration
├── docs/                     # Tài liệu
│   ├── developer_guide.md    # Hướng dẫn phát triển
│   └── troubleshooting_migrations.md # Xử lý lỗi migrations
├── tests/                    # Tests
│   ├── conftest.py           # Test fixtures
│   └── api/                  # API tests
│       └── v1/               # API v1 tests
│           ├── test_auth.py      # Auth tests
│           ├── test_location.py  # Location tests
│           ├── test_roles.py     # Roles tests
│           └── test_location_filtering.py # Filter tests
├── .env                      # Environment variables
├── alembic.ini               # Alembic configuration
├── pyproject.toml            # Poetry project definition
├── poetry.lock               # Poetry lock file
├── README.md                 # Tài liệu tổng quan dự án
└── setup_travel_app.sh       # Script thiết lập tự động
```
│       ├── 003_user_roles.py # Roles migration
│       └── 004_location_filtering.py # Location filter migration
├── tests/                    # Tests
│   ├── conftest.py           # Test fixtures
│   └── api/                  # API tests
│       └── v1/               # API v1 tests
│           ├── test_auth.py      # Auth tests
│           ├── test_location.py  # Location tests
│           ├── test_roles.py     # Roles tests
│           └── test_location_filtering.py # Filter tests
├── .env                      # Environment variables
├── alembic.ini               # Alembic configuration
├── pyproject.toml            # Poetry project definition
└── poetry.lock               # Poetry lock file
```

## Môi trường yêu cầu

- **Python 3.12+**
- **PostgreSQL** với extension **PostGIS**
- **Poetry** để quản lý dependencies
- **Docker** (khuyến nghị) cho thiết lập dễ dàng

## Thiết lập môi trường

### Phương pháp 1: Sử dụng script tự động (Khuyến nghị)

Dự án cung cấp script tự động hóa toàn bộ quá trình thiết lập môi trường:

```bash
# Cấp quyền thực thi cho script
chmod +x setup_travel_app.sh

# Chạy script thiết lập
./setup_travel_app.sh
```

Script sẽ thực hiện các bước sau:
1. Khởi chạy PostgreSQL với PostGIS trong Docker
2. Thiết lập cơ sở dữ liệu và PostGIS extension
3. Chạy Alembic migrations
4. Tùy chọn tạo dữ liệu mẫu
5. Tùy chọn khởi động ứng dụng

### Phương pháp 2: Thiết lập thủ công

#### PostgreSQL với PostGIS

##### Sử dụng Docker (Khuyến nghị)

1. Tạo và chạy container PostgreSQL với PostGIS:
   ```bash
   docker run --name postgres-postgis \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_DB=travel \
     -p 5432:5432 \
     -d postgis/postgis:14-3.3
   ```

2. Kiểm tra container đã chạy:
   ```bash
   docker ps
   ```

3. Tạo extension PostGIS trong database:
   ```bash
   docker exec -it postgres-postgis psql -U postgres -d travel -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   ```

4. Kiểm tra extension đã được cài đặt:
   ```bash
   docker exec -it postgres-postgis psql -U postgres -d travel -c "SELECT PostGIS_version();"
   ```

##### Cài đặt trực tiếp trên máy (Tùy chọn)

1. Cài đặt PostgreSQL và PostGIS:
   
   **macOS (sử dụng Homebrew):**
   ```bash
   brew install postgresql
   brew install postgis
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib postgis
   ```

2. Khởi động dịch vụ PostgreSQL:
   
   **macOS:**
   ```bash
   brew services start postgresql
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo systemctl start postgresql
   ```

3. Tạo database:
   ```bash
   psql -U postgres
   CREATE DATABASE travel;
   \c travel
   CREATE EXTENSION postgis;
   ```

### Cài đặt ứng dụng

1. Clone repository:
   ```bash
   git clone <repository_url>
   cd william-travel/backend
   ```

2. Cài đặt Poetry (nếu chưa có):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Cài đặt dependencies với Poetry:
   ```bash
   poetry install
   ```

4. Thiết lập file .env:
   ```
   # PostgreSQL Connection
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=travel
   POSTGRES_PORT=5432
   
   # General settings
   PROJECT_NAME=William Travel API
   API_V1_STR=/api/v1
   BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000","http://localhost:8080"]
   
   # Security
   SECRET_KEY=your_secret_key_here
   ACCESS_TOKEN_EXPIRE_MINUTES=11520
   
   # Email Settings
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   SMTP_FROM_EMAIL=your-email@gmail.com
   
   # Debug
   DEBUG=True
   ```

5. Thiết lập cơ sở dữ liệu:
   ```bash
   # Sử dụng script tự động để cài đặt database
   poetry run python -m app.scripts.setup_database
   ```

6. Chạy migrations:
   ```bash
   poetry run alembic upgrade head
   ```

7. Tạo dữ liệu mẫu (tùy chọn):
   ```bash
   poetry run python -m app.scripts.init_test_data
   ```

8. Khởi động server phát triển:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

9. Truy cập API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Phát triển

### Truy cập tài liệu phát triển

Dự án cung cấp tài liệu chi tiết hướng dẫn phát triển và xử lý sự cố:

1. **Hướng dẫn phát triển**:
   ```bash
   # Mở tài liệu phát triển
   open docs/developer_guide.md
   ```
   Tài liệu này cung cấp hướng dẫn đầy đủ về cách phát triển API mới có tương tác với cơ sở dữ liệu.

2. **Hướng dẫn xử lý lỗi migrations**:
   ```bash
   # Mở tài liệu xử lý sự cố migrations
   open docs/troubleshooting_migrations.md
   ```
   Tài liệu này cung cấp hướng dẫn khắc phục các vấn đề phổ biến với migrations.

### Unit Testing

Chạy tất cả các tests:
```bash
poetry run pytest
```

Chạy tests với chi tiết (verbose):
```bash
poetry run pytest -v
```

Chạy tests cho từng module cụ thể:
```bash
poetry run pytest tests/api/v1/test_location_filtering.py -v
```

### Tạo migration mới

Sau khi thay đổi model database:
```bash
# Tạo migration mới
poetry run alembic revision --autogenerate -m "mô_tả_thay_đổi"

# Áp dụng migration
poetry run alembic upgrade head
```

## Triển khai

### Triển khai với Docker Compose (Khuyến nghị)

Dự án cung cấp cấu hình Docker Compose để triển khai cả API và cơ sở dữ liệu:

1. Tạo hoặc chỉnh sửa file `docker-compose.yml`:
   ```yaml
   version: '3.8'
   
   services:
     api:
       build: .
       ports:
         - "8000:8000"
       depends_on:
         - db
       environment:
         - POSTGRES_SERVER=db
         - POSTGRES_USER=postgres
         - POSTGRES_PASSWORD=postgres
         - POSTGRES_DB=travel
         - POSTGRES_PORT=5432
         - SECRET_KEY=your_secret_key_here
         - ACCESS_TOKEN_EXPIRE_MINUTES=11520
         - PROJECT_NAME=William Travel API
         - API_V1_STR=/api/v1
       volumes:
         - ./:/app
     
     db:
       image: postgis/postgis:14-3.3
       volumes:
         - postgres_data:/var/lib/postgresql/data/
       environment:
         - POSTGRES_USER=postgres
         - POSTGRES_PASSWORD=postgres
         - POSTGRES_DB=travel
       ports:
         - "5432:5432"
   
   volumes:
     postgres_data:
   ```

2. Chạy Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Chạy migrations trong container:
   ```bash
   docker-compose exec api poetry run alembic upgrade head
   ```

4. Tạo dữ liệu mẫu (tùy chọn):
   ```bash
   docker-compose exec api poetry run python -m app.scripts.init_test_data
   ```

### Triển khai với Docker riêng lẻ

1. Build Docker image:
   ```bash
   docker build -t william-travel-backend .
   ```

2. Chạy container:
   ```bash
   docker run -d -p 8000:8000 --name william-travel-api \
     -e POSTGRES_SERVER=host.docker.internal \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_DB=travel \
     -e POSTGRES_PORT=5432 \
     william-travel-backend
   ```

## Liên hệ và đóng góp

Để đóng góp cho dự án, vui lòng tạo issue hoặc pull request.
Liên hệ: william@example.com

## License

Dự án này được phân phối dưới [MIT License](LICENSE).

### Code Quality Tools

The project includes several tools for maintaining code quality:

- **Black**: Code formatter
  ```bash
  poetry run black .
  ```

- **isort**: Import sorter
  ```bash
  poetry run isort .
  ```

- **mypy**: Static type checker
  ```bash
  poetry run mypy .
  ```

- **pytest**: Test runner
  ```bash
  poetry run pytest
  ```

### Database Migrations

Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "description_of_changes"
```

Apply migrations:

```bash
alembic upgrade head
```

Revert the last migration:

```bash
alembic downgrade -1
```

## Testing

Run all tests:

```bash
poetry run pytest
```

Run tests with coverage report:

```bash
poetry run pytest --cov=app --cov-report=term-missing
```

Run specific test file:

```bash
poetry run pytest tests/api/v1/test_location.py -v
```

## Production Deployment

For production deployment, we recommend using Gunicorn with Uvicorn workers:

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment (Optional)

1. Build the Docker image:
   ```bash
   docker build -t william-travel-backend .
   ```

2. Run the container:
   ```bash
   docker run -d --name william-travel-api -p 8000:8000 -e DATABASE_URL=your_db_url william-travel-backend
   ```

## Performance Considerations

- The application uses async SQLAlchemy for non-blocking database operations
- Connection pooling is configured for efficient database connections
- For high-load scenarios, consider:
  - Implementing caching with Redis
  - Horizontal scaling with multiple instances behind a load balancer
  - Database read replicas for read-heavy workloads

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
