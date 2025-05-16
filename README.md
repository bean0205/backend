# William Travel Backend

Backend API for William Travel application built with FastAPI, SQLAlchemy 2.x (async), and PostgreSQL with PostGIS.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0+-00a393.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.21+-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-latest-blue.svg)
![PostGIS](https://img.shields.io/badge/PostGIS-latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- **FastAPI framework** with async support for high-performance API development
- **SQLAlchemy 2.x ORM** with async capabilities for modern database interactions
- **PostgreSQL** database with **PostGIS** extension for powerful geographical data operations
- **Alembic** for database migrations with async support
- **Pydantic v2** for data validation and settings management
- **Poetry** for dependency management and packaging
- **Automatic API documentation** with Swagger UI and ReDoc
- **Async-first architecture** throughout the entire application
- **ASGI server**: Uvicorn (dev), Gunicorn + Uvicorn (prod)
- **Type hints** throughout the codebase for better IDE support and code quality

## Project Structure

```
backend/
├── app/                      # Main application package
│   ├── api/                  # API endpoints
│   │   ├── deps.py           # Dependency injection
│   │   └── v1/               # API version 1
│   │       ├── endpoints/    # API endpoints by resource
│   │       │   └── location.py  # Location endpoints
│   │       └── router.py     # API router aggregation
│   ├── core/                 # Core application components
│   │   └── config.py         # Configuration and settings
│   ├── crud/                 # CRUD operations by model
│   │   └── crud_location.py  # Location CRUD operations
│   ├── db/                   # Database related modules
│   │   ├── models.py         # SQLAlchemy models
│   │   └── session.py        # Database session management
│   ├── schemas/              # Pydantic schemas for request/response validation
│   │   └── location.py       # Location schemas
│   ├── services/             # Business logic services
│   └── main.py               # FastAPI application creation and configuration
├── alembic/                  # Database migration support
│   └── versions/             # Migration versions
│       └── 001_initial.py    # Initial database migration
├── tests/                    # Test directory
│   └── api/                  # API tests
│       └── v1/               # API v1 tests
│           └── test_location.py  # Location endpoint tests
├── .env                      # Environment variables
├── .gitignore                # Git ignore file
├── alembic.ini               # Alembic configuration
├── pyproject.toml            # Poetry project definition
└── poetry.lock               # Poetry lock file with exact versions
```

## Prerequisites

- **Python 3.11+**
- **PostgreSQL** with **PostGIS** extension
- **Poetry** for dependency management
- Optional: Docker for containerized deployment

## Environment Setup

### PostgreSQL with PostGIS

1. Install PostgreSQL and PostGIS:
   
   **macOS (using Homebrew):**
   ```bash
   brew install postgresql
   brew install postgis
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib postgis postgresql-14-postgis-3
   ```

2. Start PostgreSQL service:
   
   **macOS:**
   ```bash
   brew services start postgresql
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo systemctl start postgresql
   ```

3. Create the database:
   ```bash
   psql -U postgres
   ```
   
   ```sql
   CREATE DATABASE william_travel_db;
   \c william_travel_db
   CREATE EXTENSION postgis;
   ```

### Python Environment

1. Install Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/william-travel-backend.git
   cd william-travel-backend
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Configure environment variables:
   - Use the provided `.env` file or create one based on your settings
   - Modify database credentials as needed

## Application Setup and Running

1. Activate the poetry environment:
   ```bash
   poetry shell
   ```

2. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Access the application:
   - API: http://localhost:8000/api/v1/
   - Swagger UI documentation: http://localhost:8000/docs
   - ReDoc alternative documentation: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

## API Endpoints

### Locations

| Method | Endpoint | Description | Query Parameters |
|--------|----------|-------------|-----------------|
| `GET` | `/api/v1/locations/` | List all locations | `skip`, `limit`, `search`, `is_active` |
| `POST` | `/api/v1/locations/` | Create a new location | - |
| `GET` | `/api/v1/locations/{location_id}` | Get a specific location | - |
| `PUT` | `/api/v1/locations/{location_id}` | Update a specific location | - |
| `DELETE` | `/api/v1/locations/{location_id}` | Delete a specific location | - |

### Location Schema

```json
{
  "name": "String (required)",
  "description": "String (optional)",
  "latitude": "Float (required)",
  "longitude": "Float (required)",
  "address": "String (optional)",
  "city": "String (optional)",
  "country": "String (optional)",
  "is_active": "Boolean (default: true)"
}
```

## Development Workflow

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
