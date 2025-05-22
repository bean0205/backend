import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app import crud
from app.schemas.food import FoodCreate, FoodUpdate


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
    """Create a test location for foods"""
    from app.schemas.location import LocationCreate

    location_data = LocationCreate(
        name="Food Test Location",
        country="Food Country",
        latitude=40.7128,
        longitude=-74.0060,
        description="A location known for its cuisine",
        continent="North America",
        is_active=True
    )
    location = await crud.location.create(db, obj_in=location_data)
    return location


@pytest.fixture
async def create_test_food(db: AsyncSession, create_test_location):
    """Create a test food item"""
    food_data = FoodCreate(
        name="Test Dish",
        description="A delicious test dish",
        location_id=create_test_location.id,
        cuisine_type="Local",
        price=15.00,
        ingredients=["ingredient1", "ingredient2"],
        dietary_restrictions=["vegetarian"],
        is_active=True
    )
    food = await crud.food.create(db, obj_in=food_data)
    return food


@pytest.mark.asyncio
async def test_create_food(client: AsyncClient, admin_token_headers, create_test_location):
    """Test creating a new food item"""
    food_data = {
        "name": "Pasta Carbonara",
        "description": "Classic Italian pasta dish",
        "location_id": create_test_location.id,
        "cuisine_type": "Italian",
        "price": 12.50,
        "ingredients": ["pasta", "eggs", "cheese", "bacon"],
        "dietary_restrictions": [],
        "is_active": True
    }

    response = await client.post(
        "/api/v1/foods/",
        headers=admin_token_headers,
        json=food_data
    )

    assert response.status_code == status.HTTP_200_OK
    created_food = response.json()
    assert created_food["name"] == "Pasta Carbonara"
    assert created_food["cuisine_type"] == "Italian"
    assert created_food["price"] == 12.50
    assert "pasta" in created_food["ingredients"]
    assert created_food["location_id"] == create_test_location.id


@pytest.mark.asyncio
async def test_read_foods(client: AsyncClient, create_test_food):
    """Test retrieving all foods (public endpoint)"""
    response = await client.get("/api/v1/foods/")

    assert response.status_code == status.HTTP_200_OK
    foods = response.json()
    assert len(foods) >= 1
    assert any(food["name"] == "Test Dish" for food in foods)


@pytest.mark.asyncio
async def test_read_foods_with_filters(client: AsyncClient, create_test_food):
    """Test retrieving foods with filters"""
    # Filter by cuisine type
    response = await client.get("/api/v1/foods/?cuisine_type=Local")

    assert response.status_code == status.HTTP_200_OK
    foods = response.json()
    assert all(food["cuisine_type"] == "Local" for food in foods)

    # Filter by price range
    response = await client.get("/api/v1/foods/?min_price=10&max_price=20")

    assert response.status_code == status.HTTP_200_OK
    foods = response.json()
    assert all(10 <= food["price"] <= 20 for food in foods)

    # Filter by dietary restrictions
    response = await client.get("/api/v1/foods/?dietary_restriction=vegetarian")

    assert response.status_code == status.HTTP_200_OK
    foods = response.json()
    assert all("vegetarian" in food["dietary_restrictions"] for food in foods)


@pytest.mark.asyncio
async def test_read_foods_by_location(client: AsyncClient, create_test_food, create_test_location):
    """Test retrieving foods by location ID"""
    location_id = create_test_location.id

    response = await client.get(f"/api/v1/foods/location/{location_id}")

    assert response.status_code == status.HTTP_200_OK
    foods = response.json()
    assert len(foods) >= 1
    assert all(food["location_id"] == location_id for food in foods)


@pytest.mark.asyncio
async def test_search_foods(client: AsyncClient, create_test_food):
    """Test searching foods by query"""
    response = await client.get("/api/v1/foods/search?query=delicious")

    assert response.status_code == status.HTTP_200_OK
    foods = response.json()
    assert len(foods) >= 1
    assert any("delicious" in food["description"].lower() for food in foods)


@pytest.mark.asyncio
async def test_read_food(client: AsyncClient, create_test_food):
    """Test retrieving a food by ID"""
    food_id = create_test_food.id

    response = await client.get(f"/api/v1/foods/{food_id}")

    assert response.status_code == status.HTTP_200_OK
    food = response.json()
    assert food["id"] == food_id
    assert food["name"] == "Test Dish"
    assert food["price"] == 15.00
    assert "vegetarian" in food["dietary_restrictions"]


@pytest.mark.asyncio
async def test_read_food_not_found(client: AsyncClient):
    """Test retrieving a non-existent food"""
    response = await client.get("/api/v1/foods/999999")  # Non-existent ID

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_food(client: AsyncClient, admin_token_headers, create_test_food):
    """Test updating a food item"""
    food_id = create_test_food.id
    update_data = {
        "name": "Updated Dish Name",
        "price": 18.50,
        "ingredients": ["ingredient1", "ingredient2", "ingredient3"],
        "dietary_restrictions": ["vegetarian", "gluten-free"]
    }

    response = await client.put(
        f"/api/v1/foods/{food_id}",
        headers=admin_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_200_OK
    updated_food = response.json()
    assert updated_food["name"] == "Updated Dish Name"
    assert updated_food["price"] == 18.50
    assert "ingredient3" in updated_food["ingredients"]
    assert "gluten-free" in updated_food["dietary_restrictions"]


@pytest.mark.asyncio
async def test_update_food_not_found(client: AsyncClient, admin_token_headers):
    """Test updating a non-existent food"""
    update_data = {
        "name": "Non-existent Food",
        "price": 25.00
    }

    response = await client.put(
        "/api/v1/foods/999999",  # Non-existent ID
        headers=admin_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_food(client: AsyncClient, admin_token_headers, create_test_food):
    """Test deleting a food item"""
    food_id = create_test_food.id

    response = await client.delete(
        f"/api/v1/foods/{food_id}",
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_200_OK

    # Verify food no longer exists or is marked as inactive
    get_response = await client.get(f"/api/v1/foods/{food_id}")

    # Either it should return 404 or the food should be marked as inactive
    if get_response.status_code == status.HTTP_200_OK:
        food = get_response.json()
        assert food["is_active"] is False
    else:
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_unauthorized_food_operations(client: AsyncClient, create_test_food):
    """Test that protected food operations require authentication"""
    food_id = create_test_food.id

    # Try to create without auth
    create_data = {
        "name": "Unauthorized Dish",
        "description": "Shouldn't be created",
        "location_id": 1,
        "price": 10.00
    }
    response = await client.post("/api/v1/foods/", json=create_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to update without auth
    update_data = {"name": "Updated Name"}
    response = await client.put(f"/api/v1/foods/{food_id}", json=update_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to delete without auth
    response = await client.delete(f"/api/v1/foods/{food_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
