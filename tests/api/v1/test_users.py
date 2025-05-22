import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app import crud
from app.schemas.user import UserCreate, UserUpdate


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
async def create_test_user(db: AsyncSession):
    """Create a regular test user"""
    user_data = UserCreate(
        email="user@test.com",
        password="user_password123",
        full_name="Test User"
    )
    user = await crud.user.create(db, obj_in=user_data)
    return user


@pytest.fixture
async def user_token_headers(client: AsyncClient, create_test_user):
    """Get token headers for regular user"""
    login_data = {
        "username": "user@test.com",
        "password": "user_password123",
    }
    response = await client.post("/api/v1/auth/login", data=login_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, admin_token_headers):
    """Test creating a new user"""
    user_data = {
        "email": "newuser@test.com",
        "password": "newuser_password123",
        "full_name": "New Test User"
    }

    response = await client.post(
        "/api/v1/users/",
        headers=admin_token_headers,
        json=user_data
    )

    assert response.status_code == status.HTTP_200_OK
    created_user = response.json()
    assert created_user["email"] == "newuser@test.com"
    assert created_user["full_name"] == "New Test User"
    assert "password" not in created_user  # Password should not be in response


@pytest.mark.asyncio
async def test_create_user_existing_email(client: AsyncClient, admin_token_headers, create_test_user):
    """Test creating a user with existing email (should fail)"""
    user_data = {
        "email": "user@test.com",  # Same email as fixture
        "password": "another_password123",
        "full_name": "Another User"
    }

    response = await client.post(
        "/api/v1/users/",
        headers=admin_token_headers,
        json=user_data
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_read_users(client: AsyncClient, admin_token_headers, create_test_user):
    """Test retrieving all users"""
    response = await client.get(
        "/api/v1/users/",
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) >= 2  # Admin user + test user
    assert any(user["email"] == "user@test.com" for user in users)
    assert any(user["email"] == "admin@test.com" for user in users)


@pytest.mark.asyncio
async def test_read_user(client: AsyncClient, admin_token_headers, create_test_user):
    """Test retrieving a user by ID"""
    user_id = create_test_user.id

    response = await client.get(
        f"/api/v1/users/{user_id}",
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["id"] == user_id
    assert user["email"] == "user@test.com"
    assert user["full_name"] == "Test User"
    assert "password" not in user


@pytest.mark.asyncio
async def test_read_user_not_found(client: AsyncClient, admin_token_headers):
    """Test retrieving a non-existent user"""
    response = await client.get(
        "/api/v1/users/999999",  # Non-existent ID
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_read_user_me(client: AsyncClient, user_token_headers, create_test_user):
    """Test retrieving own user data"""
    response = await client.get(
        "/api/v1/users/me",
        headers=user_token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["email"] == "user@test.com"
    assert user["full_name"] == "Test User"
    assert "password" not in user


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, admin_token_headers, create_test_user):
    """Test updating a user"""
    user_id = create_test_user.id
    update_data = {
        "full_name": "Updated User Name"
    }

    response = await client.put(
        f"/api/v1/users/{user_id}",
        headers=admin_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_200_OK
    updated_user = response.json()
    assert updated_user["full_name"] == "Updated User Name"
    assert updated_user["email"] == "user@test.com"


@pytest.mark.asyncio
async def test_update_user_me(client: AsyncClient, user_token_headers):
    """Test updating own user data"""
    update_data = {
        "full_name": "My New Name"
    }

    response = await client.put(
        "/api/v1/users/me",
        headers=user_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_200_OK
    updated_user = response.json()
    assert updated_user["full_name"] == "My New Name"


@pytest.mark.asyncio
async def test_update_user_password(client: AsyncClient, user_token_headers):
    """Test updating own password"""
    password_data = {
        "current_password": "user_password123",
        "new_password": "new_password123"
    }

    response = await client.put(
        "/api/v1/users/me/password",
        headers=user_token_headers,
        json=password_data
    )

    assert response.status_code == status.HTTP_200_OK

    # Test login with new password
    login_data = {
        "username": "user@test.com",
        "password": "new_password123",
    }
    login_response = await client.post("/api/v1/auth/login", data=login_data)
    assert login_response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, admin_token_headers, create_test_user):
    """Test deleting a user"""
    user_id = create_test_user.id

    response = await client.delete(
        f"/api/v1/users/{user_id}",
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_200_OK

    # Verify user no longer exists
    get_response = await client.get(
        f"/api/v1/users/{user_id}",
        headers=admin_token_headers
    )

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test accessing users endpoints without authentication"""
    response = await client.get("/api/v1/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = await client.post("/api/v1/users/", json={"email": "test@example.com"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
