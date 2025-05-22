import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app import crud
from app.schemas.location import LocationCreate, LocationUpdate


@pytest.fixture
async def create_test_admin_user(db: AsyncSession):
    """Create a superuser for testing protected endpoints"""
    from app.schemas.user import UserCreate

    admin_data = UserCreate(
        email="admin@test.com",
        password="admin_password123",
        is_superuser=True,
        full_name="Test Admin"
    )
    admin_user = await crud.user.create(db, obj_in=admin_data)
    return admin_user


@pytest.fixture
async def admin_token_headers(client: AsyncClient, create_test_admin_user):
    """Get token headers for admin user"""
    login_data = {
        "username": "admin@test.com",
        "password": "admin_password123",
    }
    response = await client.post("/api/v1/auth/login", data=login_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture
async def create_test_location(db: AsyncSession):
    """Create a test location"""
    location_data = LocationCreate(
        name="Test City",
        country="Test Country",
        latitude=35.6812,
        longitude=139.7671,
        description="A beautiful test city for travelers",
        continent="Asia",
        is_active=True
    )
    location = await crud.location.create(db, obj_in=location_data)
    return location


@pytest.mark.asyncio
async def test_create_location(client: AsyncClient, admin_token_headers):
    """Test creating a new location"""
    location_data = {
        "name": "Paris",
        "country": "France",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "description": "The city of lights and romance",
        "continent": "Europe",
        "is_active": True
    }

    response = await client.post(
        "/api/v1/locations/",
        headers=admin_token_headers,
        json=location_data
    )

    assert response.status_code == status.HTTP_200_OK
    created_location = response.json()
    assert created_location["name"] == "Paris"
    assert created_location["country"] == "France"
    assert created_location["continent"] == "Europe"
    assert abs(created_location["latitude"] - 48.8566) < 0.001
    assert abs(created_location["longitude"] - 2.3522) < 0.001


@pytest.mark.asyncio
async def test_read_locations(client: AsyncClient, create_test_location):
    """Test retrieving all locations (public endpoint)"""
    response = await client.get("/api/v1/locations/")

    assert response.status_code == status.HTTP_200_OK
    locations = response.json()
    assert len(locations) >= 1
    assert any(loc["name"] == "Test City" for loc in locations)


@pytest.mark.asyncio
async def test_read_locations_with_filters(client: AsyncClient, create_test_location):
    """Test retrieving locations with filters"""
    # Filter by continent
    response = await client.get("/api/v1/locations/?continent=Asia")

    assert response.status_code == status.HTTP_200_OK
    locations = response.json()
    assert all(loc["continent"] == "Asia" for loc in locations)

    # Filter by country
    response = await client.get("/api/v1/locations/?country=Test%20Country")

    assert response.status_code == status.HTTP_200_OK
    locations = response.json()
    assert all(loc["country"] == "Test Country" for loc in locations)


@pytest.mark.asyncio
async def test_search_locations(client: AsyncClient, create_test_location):
    """Test searching locations by name or description"""
    response = await client.get("/api/v1/locations/search?query=beautiful")

    assert response.status_code == status.HTTP_200_OK
    locations = response.json()
    assert len(locations) >= 1
    assert any("beautiful" in loc["description"].lower() for loc in locations)


@pytest.mark.asyncio
async def test_read_location(client: AsyncClient, create_test_location):
    """Test retrieving a location by ID"""
    location_id = create_test_location.id

    response = await client.get(f"/api/v1/locations/{location_id}")

    assert response.status_code == status.HTTP_200_OK
    location = response.json()
    assert location["id"] == location_id
    assert location["name"] == "Test City"
    assert location["country"] == "Test Country"


@pytest.mark.asyncio
async def test_read_location_not_found(client: AsyncClient):
    """Test retrieving a non-existent location"""
    response = await client.get("/api/v1/locations/999999")  # Non-existent ID

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_location(client: AsyncClient, admin_token_headers, create_test_location):
    """Test updating a location"""
    location_id = create_test_location.id
    update_data = {
        "name": "Updated City Name",
        "description": "Updated description"
    }

    response = await client.put(
        f"/api/v1/locations/{location_id}",
        headers=admin_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_200_OK
    updated_location = response.json()
    assert updated_location["name"] == "Updated City Name"
    assert updated_location["description"] == "Updated description"
    assert updated_location["country"] == "Test Country"  # Unchanged field


@pytest.mark.asyncio
async def test_update_location_not_found(client: AsyncClient, admin_token_headers):
    """Test updating a non-existent location"""
    update_data = {
        "name": "Non-existent Location",
        "description": "This location doesn't exist"
    }

    response = await client.put(
        "/api/v1/locations/999999",  # Non-existent ID
        headers=admin_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_location(client: AsyncClient, admin_token_headers, create_test_location):
    """Test deleting a location"""
    location_id = create_test_location.id

    response = await client.delete(
        f"/api/v1/locations/{location_id}",
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_200_OK

    # Verify location no longer exists or is marked as inactive
    get_response = await client.get(f"/api/v1/locations/{location_id}")

    # Either it should return 404 or the location should be marked as inactive
    if get_response.status_code == status.HTTP_200_OK:
        location = get_response.json()
        assert location["is_active"] is False
    else:
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_location_by_coordinates(client: AsyncClient, create_test_location):
    """Test finding locations near specific coordinates"""
    lat = 35.6812
    lon = 139.7671
    radius = 10  # km

    response = await client.get(
        f"/api/v1/locations/nearby?latitude={lat}&longitude={lon}&radius={radius}"
    )

    assert response.status_code == status.HTTP_200_OK
    locations = response.json()
    assert len(locations) >= 1

    # Verify that returned locations are within the specified radius
    for loc in locations:
        # Calculate approximate distance (simplified for testing)
        lat_diff = abs(loc["latitude"] - lat)
        lon_diff = abs(loc["longitude"] - lon)
        approx_distance = (lat_diff ** 2 + lon_diff ** 2) ** 0.5 * 111  # Rough conversion to km
        assert approx_distance <= radius


@pytest.mark.asyncio
async def test_unauthorized_location_operations(client: AsyncClient, create_test_location):
    """Test that protected location operations require authentication"""
    location_id = create_test_location.id

    # Try to create without auth
    create_data = {
        "name": "Unauthorized City",
        "country": "Unauthorized Country",
        "latitude": 0,
        "longitude": 0
    }
    response = await client.post("/api/v1/locations/", json=create_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to update without auth
    update_data = {"name": "Updated Name"}
    response = await client.put(f"/api/v1/locations/{location_id}", json=update_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to delete without auth
    response = await client.delete(f"/api/v1/locations/{location_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
