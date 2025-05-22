import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app import crud
from app.schemas.accommodation import AccommodationCreate, AccommodationUpdate


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
    """Create a test location for accommodations"""
    from app.schemas.location import LocationCreate

    location_data = LocationCreate(
        name="Test Location",
        country="Test Country",
        latitude=35.6812,
        longitude=139.7671,
        description="A test location",
        continent="Asia",
        is_active=True
    )
    location = await crud.location.create(db, obj_in=location_data)
    return location


@pytest.fixture
async def create_test_accommodation(db: AsyncSession, create_test_location):
    """Create a test accommodation"""
    accommodation_data = AccommodationCreate(
        name="Test Hotel",
        description="A comfortable test hotel",
        location_id=create_test_location.id,
        price_per_night=100.0,
        accommodation_type="hotel",
        amenities=["wifi", "pool", "breakfast"],
        address="123 Test Street",
        is_active=True
    )
    accommodation = await crud.accommodation.create(db, obj_in=accommodation_data)
    return accommodation


@pytest.mark.asyncio
async def test_create_accommodation(client: AsyncClient, admin_token_headers, create_test_location):
    """Test creating a new accommodation"""
    accommodation_data = {
        "name": "Luxury Resort",
        "description": "A luxury resort with amazing views",
        "location_id": create_test_location.id,
        "price_per_night": 250.0,
        "accommodation_type": "resort",
        "amenities": ["wifi", "pool", "spa", "restaurant"],
        "address": "789 Resort Boulevard",
        "is_active": True
    }

    response = await client.post(
        "/api/v1/accommodations/",
        headers=admin_token_headers,
        json=accommodation_data
    )

    assert response.status_code == status.HTTP_200_OK
    created_accommodation = response.json()
    assert created_accommodation["name"] == "Luxury Resort"
    assert created_accommodation["price_per_night"] == 250.0
    assert "spa" in created_accommodation["amenities"]
    assert created_accommodation["location_id"] == create_test_location.id


@pytest.mark.asyncio
async def test_read_accommodations(client: AsyncClient, create_test_accommodation):
    """Test retrieving all accommodations (public endpoint)"""
    response = await client.get("/api/v1/accommodations/")

    assert response.status_code == status.HTTP_200_OK
    accommodations = response.json()
    assert len(accommodations) >= 1
    assert any(acc["name"] == "Test Hotel" for acc in accommodations)


@pytest.mark.asyncio
async def test_read_accommodations_with_filters(client: AsyncClient, create_test_accommodation):
    """Test retrieving accommodations with filters"""
    # Filter by accommodation type
    response = await client.get("/api/v1/accommodations/?accommodation_type=hotel")

    assert response.status_code == status.HTTP_200_OK
    accommodations = response.json()
    assert all(acc["accommodation_type"] == "hotel" for acc in accommodations)

    # Filter by price range
    response = await client.get("/api/v1/accommodations/?min_price=50&max_price=150")

    assert response.status_code == status.HTTP_200_OK
    accommodations = response.json()
    assert all(50 <= acc["price_per_night"] <= 150 for acc in accommodations)


@pytest.mark.asyncio
async def test_read_accommodations_by_location(client: AsyncClient, create_test_accommodation, create_test_location):
    """Test retrieving accommodations by location ID"""
    location_id = create_test_location.id

    response = await client.get(f"/api/v1/accommodations/location/{location_id}")

    assert response.status_code == status.HTTP_200_OK
    accommodations = response.json()
    assert len(accommodations) >= 1
    assert all(acc["location_id"] == location_id for acc in accommodations)


@pytest.mark.asyncio
async def test_search_accommodations(client: AsyncClient, create_test_accommodation):
    """Test searching accommodations by query"""
    response = await client.get("/api/v1/accommodations/search?query=comfortable")

    assert response.status_code == status.HTTP_200_OK
    accommodations = response.json()
    assert len(accommodations) >= 1
    assert any("comfortable" in acc["description"].lower() for acc in accommodations)


@pytest.mark.asyncio
async def test_read_accommodation(client: AsyncClient, create_test_accommodation):
    """Test retrieving an accommodation by ID"""
    accommodation_id = create_test_accommodation.id

    response = await client.get(f"/api/v1/accommodations/{accommodation_id}")

    assert response.status_code == status.HTTP_200_OK
    accommodation = response.json()
    assert accommodation["id"] == accommodation_id
    assert accommodation["name"] == "Test Hotel"
    assert accommodation["price_per_night"] == 100.0


@pytest.mark.asyncio
async def test_read_accommodation_not_found(client: AsyncClient):
    """Test retrieving a non-existent accommodation"""
    response = await client.get("/api/v1/accommodations/999999")  # Non-existent ID

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_accommodation(client: AsyncClient, admin_token_headers, create_test_accommodation):
    """Test updating an accommodation"""
    accommodation_id = create_test_accommodation.id
    update_data = {
        "name": "Updated Hotel Name",
        "price_per_night": 120.0,
        "amenities": ["wifi", "pool", "breakfast", "gym"]
    }

    response = await client.put(
        f"/api/v1/accommodations/{accommodation_id}",
        headers=admin_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_200_OK
    updated_accommodation = response.json()
    assert updated_accommodation["name"] == "Updated Hotel Name"
    assert updated_accommodation["price_per_night"] == 120.0
    assert "gym" in updated_accommodation["amenities"]


@pytest.mark.asyncio
async def test_update_accommodation_not_found(client: AsyncClient, admin_token_headers):
    """Test updating a non-existent accommodation"""
    update_data = {
        "name": "Non-existent Accommodation",
        "price_per_night": 150.0
    }

    response = await client.put(
        "/api/v1/accommodations/999999",  # Non-existent ID
        headers=admin_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_accommodation(client: AsyncClient, admin_token_headers, create_test_accommodation):
    """Test deleting an accommodation"""
    accommodation_id = create_test_accommodation.id

    response = await client.delete(
        f"/api/v1/accommodations/{accommodation_id}",
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_200_OK

    # Verify accommodation no longer exists or is marked as inactive
    get_response = await client.get(f"/api/v1/accommodations/{accommodation_id}")

    # Either it should return 404 or the accommodation should be marked as inactive
    if get_response.status_code == status.HTTP_200_OK:
        accommodation = get_response.json()
        assert accommodation["is_active"] is False
    else:
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_unauthorized_accommodation_operations(client: AsyncClient, create_test_accommodation):
    """Test that protected accommodation operations require authentication"""
    accommodation_id = create_test_accommodation.id

    # Try to create without auth
    create_data = {
        "name": "Unauthorized Hotel",
        "description": "Shouldn't be created",
        "location_id": 1,
        "price_per_night": 100.0
    }
    response = await client.post("/api/v1/accommodations/", json=create_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to update without auth
    update_data = {"name": "Updated Name"}
    response = await client.put(f"/api/v1/accommodations/{accommodation_id}", json=update_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to delete without auth
    response = await client.delete(f"/api/v1/accommodations/{accommodation_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
