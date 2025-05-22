import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app import crud
from app.schemas.rating import RatingCreate, RatingUpdate


@pytest.fixture
async def create_test_user(db: AsyncSession):
    """Create a regular test user for ratings"""
    from app.schemas.user import UserCreate

    user_data = UserCreate(
        email="rating_user@test.com",
        password="rating_password123",
        full_name="Rating Test User"
    )
    user = await crud.user.create(db, obj_in=user_data)
    return user


@pytest.fixture
async def user_token_headers(client: AsyncClient, create_test_user):
    """Get token headers for regular user"""
    login_data = {
        "username": "rating_user@test.com",
        "password": "rating_password123",
    }
    response = await client.post("/api/v1/auth/login", data=login_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture
async def create_test_location(db: AsyncSession):
    """Create a test location for ratings"""
    from app.schemas.location import LocationCreate

    location_data = LocationCreate(
        name="Rating Test Location",
        country="Test Country",
        latitude=41.8781,
        longitude=-87.6298,
        description="A location for testing ratings",
        continent="North America",
        is_active=True
    )
    location = await crud.location.create(db, obj_in=location_data)
    return location


@pytest.fixture
async def create_test_rating(db: AsyncSession, create_test_user, create_test_location):
    """Create a test rating"""
    rating_data = RatingCreate(
        user_id=create_test_user.id,
        entity_id=create_test_location.id,
        entity_type="location",
        rating=4,
        review="This is a good test location",
        is_active=True
    )
    rating = await crud.rating.create(db, obj_in=rating_data)
    return rating


@pytest.mark.asyncio
async def test_create_rating(client: AsyncClient, user_token_headers, create_test_location, create_test_user):
    """Test creating a new rating"""
    rating_data = {
        "entity_id": create_test_location.id,
        "entity_type": "location",
        "rating": 5,
        "review": "Amazing place, highly recommended!"
    }

    response = await client.post(
        "/api/v1/ratings/",
        headers=user_token_headers,
        json=rating_data
    )

    assert response.status_code == status.HTTP_200_OK
    created_rating = response.json()
    assert created_rating["entity_id"] == create_test_location.id
    assert created_rating["entity_type"] == "location"
    assert created_rating["rating"] == 5
    assert created_rating["review"] == "Amazing place, highly recommended!"
    assert created_rating["user_id"] == create_test_user.id


@pytest.mark.asyncio
async def test_read_ratings(client: AsyncClient, create_test_rating):
    """Test retrieving all ratings (public endpoint)"""
    response = await client.get("/api/v1/ratings/")

    assert response.status_code == status.HTTP_200_OK
    ratings = response.json()
    assert len(ratings) >= 1
    assert any(rating["review"] == "This is a good test location" for rating in ratings)


@pytest.mark.asyncio
async def test_read_ratings_by_entity(client: AsyncClient, create_test_rating, create_test_location):
    """Test retrieving ratings by entity type and ID"""
    entity_id = create_test_location.id

    response = await client.get(f"/api/v1/ratings/entity/location/{entity_id}")

    assert response.status_code == status.HTTP_200_OK
    ratings = response.json()
    assert len(ratings) >= 1
    assert all(rating["entity_id"] == entity_id for rating in ratings)
    assert all(rating["entity_type"] == "location" for rating in ratings)


@pytest.mark.asyncio
async def test_read_ratings_by_user(client: AsyncClient, user_token_headers, create_test_rating, create_test_user):
    """Test retrieving ratings by user"""
    user_id = create_test_user.id

    response = await client.get(
        f"/api/v1/ratings/user/{user_id}",
        headers=user_token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    ratings = response.json()
    assert len(ratings) >= 1
    assert all(rating["user_id"] == user_id for rating in ratings)


@pytest.mark.asyncio
async def test_read_own_ratings(client: AsyncClient, user_token_headers, create_test_rating):
    """Test retrieving own ratings"""
    response = await client.get(
        "/api/v1/ratings/me",
        headers=user_token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    ratings = response.json()
    assert len(ratings) >= 1
    assert all(rating["review"] == "This is a good test location" for rating in ratings)


@pytest.mark.asyncio
async def test_read_rating(client: AsyncClient, create_test_rating):
    """Test retrieving a rating by ID"""
    rating_id = create_test_rating.id

    response = await client.get(f"/api/v1/ratings/{rating_id}")

    assert response.status_code == status.HTTP_200_OK
    rating = response.json()
    assert rating["id"] == rating_id
    assert rating["rating"] == 4
    assert rating["review"] == "This is a good test location"


@pytest.mark.asyncio
async def test_read_rating_not_found(client: AsyncClient):
    """Test retrieving a non-existent rating"""
    response = await client.get("/api/v1/ratings/999999")  # Non-existent ID

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_rating(client: AsyncClient, user_token_headers, create_test_rating):
    """Test updating own rating"""
    rating_id = create_test_rating.id
    update_data = {
        "rating": 3,
        "review": "Updated review after second visit"
    }

    response = await client.put(
        f"/api/v1/ratings/{rating_id}",
        headers=user_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_200_OK
    updated_rating = response.json()
    assert updated_rating["rating"] == 3
    assert updated_rating["review"] == "Updated review after second visit"


@pytest.mark.asyncio
async def test_update_rating_not_found(client: AsyncClient, user_token_headers):
    """Test updating a non-existent rating"""
    update_data = {
        "rating": 2,
        "review": "This shouldn't update anything"
    }

    response = await client.put(
        "/api/v1/ratings/999999",  # Non-existent ID
        headers=user_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_rating(client: AsyncClient, user_token_headers, create_test_rating):
    """Test deleting own rating"""
    rating_id = create_test_rating.id

    response = await client.delete(
        f"/api/v1/ratings/{rating_id}",
        headers=user_token_headers
    )

    assert response.status_code == status.HTTP_200_OK

    # Verify rating no longer exists or is marked as inactive
    get_response = await client.get(f"/api/v1/ratings/{rating_id}")

    # Either it should return 404 or the rating should be marked as inactive
    if get_response.status_code == status.HTTP_200_OK:
        rating = get_response.json()
        assert rating["is_active"] is False
    else:
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_unauthorized_rating_operations(client: AsyncClient, create_test_rating):
    """Test that protected rating operations require authentication"""
    rating_id = create_test_rating.id

    # Try to create without auth
    create_data = {
        "entity_id": 1,
        "entity_type": "location",
        "rating": 5,
        "review": "This should fail"
    }
    response = await client.post("/api/v1/ratings/", json=create_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to update without auth
    update_data = {"rating": 1, "review": "Unauthorized update"}
    response = await client.put(f"/api/v1/ratings/{rating_id}", json=update_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to delete without auth
    response = await client.delete(f"/api/v1/ratings/{rating_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_other_user_cannot_modify_rating(client: AsyncClient, create_test_rating):
    """Test that users cannot modify other users' ratings"""
    # Create second user
    from app.schemas.user import UserCreate

    async def create_another_user(client: AsyncClient, db: AsyncSession):
        user_data = UserCreate(
            email="another_user@test.com",
            password="another_password123",
            full_name="Another Test User"
        )
        user = await crud.user.create(db, obj_in=user_data)

        # Login
        login_data = {
            "username": "another_user@test.com",
            "password": "another_password123",
        }
        login_response = await client.post("/api/v1/auth/login", data=login_data)
        tokens = login_response.json()
        return {"Authorization": f"Bearer {tokens['access_token']}"}

    db_session = next(crud.get_db())
    other_user_headers = await create_another_user(client, db_session)

    rating_id = create_test_rating.id
    update_data = {"rating": 1, "review": "Trying to modify someone else's rating"}

    # Try to update other user's rating
    response = await client.put(
        f"/api/v1/ratings/{rating_id}",
        headers=other_user_headers,
        json=update_data
    )

    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]

    # Try to delete other user's rating
    response = await client.delete(
        f"/api/v1/ratings/{rating_id}",
        headers=other_user_headers
    )

    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
