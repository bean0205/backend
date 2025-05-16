import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.session import Base, get_db
from app.main import app
from app.db.models import Location


# Use an in-memory SQLite database for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# Override the get_db dependency to use the test database
async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
async def test_db():
    # Create the test database and tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # Run the tests
    
    # Drop the tables after the tests are complete
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(test_db) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_location(test_db) -> Location:
    # Create a test location
    async with TestingSessionLocal() as session:
        location = Location(
            name="Test Location",
            description="This is a test location",
            latitude=40.7128,
            longitude=-74.0060,
            geom="SRID=4326;POINT(-74.0060 40.7128)",  # WKT format for geometry
            address="Test Address",
            city="New York",
            country="USA",
            is_active=True
        )
        session.add(location)
        await session.commit()
        await session.refresh(location)
        return location


@pytest.mark.asyncio
async def test_read_locations(client: AsyncClient):
    response = await client.get("/api/v1/locations/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_create_location(client: AsyncClient):
    location_data = {
        "name": "New Test Location",
        "description": "This is a new test location",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "address": "Test Address 2",
        "city": "Paris",
        "country": "France",
        "is_active": True
    }
    response = await client.post("/api/v1/locations/", json=location_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == location_data["name"]
    assert data["latitude"] == location_data["latitude"]
    assert data["longitude"] == location_data["longitude"]


@pytest.mark.asyncio
async def test_read_location(client: AsyncClient, test_location: Location):
    response = await client.get(f"/api/v1/locations/{test_location.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_location.id
    assert data["name"] == test_location.name


@pytest.mark.asyncio
async def test_update_location(client: AsyncClient, test_location: Location):
    update_data = {"name": "Updated Test Location"}
    response = await client.put(
        f"/api/v1/locations/{test_location.id}", 
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]


@pytest.mark.asyncio
async def test_delete_location(client: AsyncClient, test_location: Location):
    response = await client.delete(f"/api/v1/locations/{test_location.id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    response = await client.get(f"/api/v1/locations/{test_location.id}")
    assert response.status_code == 404
