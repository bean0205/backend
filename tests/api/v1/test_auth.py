import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app import crud
from app.schemas.user import UserCreate


@pytest.fixture
async def create_test_user(db: AsyncSession):
    """Create a test user for authentication tests"""
    user_data = UserCreate(
        email="auth_user@test.com",
        password="auth_password123",
        full_name="Authentication Test User"
    )
    user = await crud.user.create(db, obj_in=user_data)
    return user


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, create_test_user):
    """Test successful login with correct credentials"""
    login_data = {
        "username": "auth_user@test.com",
        "password": "auth_password123",
    }

    response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )

    assert response.status_code == status.HTTP_200_OK
    tokens = response.json()
    assert "access_token" in tokens
    assert "token_type" in tokens
    assert tokens["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, create_test_user):
    """Test login with wrong password"""
    login_data = {
        "username": "auth_user@test.com",
        "password": "wrong_password",
    }

    response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Test login with nonexistent user"""
    login_data = {
        "username": "nonexistent@test.com",
        "password": "some_password",
    }

    response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration"""
    register_data = {
        "email": "new_register@test.com",
        "password": "register_password123",
        "full_name": "Newly Registered User"
    }

    response = await client.post(
        "/api/v1/auth/register",
        json=register_data
    )

    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["email"] == "new_register@test.com"
    assert user["full_name"] == "Newly Registered User"
    assert "password" not in user


@pytest.mark.asyncio
async def test_register_existing_user(client: AsyncClient, create_test_user):
    """Test registration with an existing email"""
    register_data = {
        "email": "auth_user@test.com",  # Same as fixture
        "password": "another_password",
        "full_name": "Duplicate User"
    }

    response = await client.post(
        "/api/v1/auth/register",
        json=register_data
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, create_test_user):
    """Test token refresh functionality"""
    # First login to get tokens
    login_data = {
        "username": "auth_user@test.com",
        "password": "auth_password123",
    }

    login_response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )

    tokens = login_response.json()
    refresh_token = tokens["refresh_token"]

    # Use refresh token to get new access token
    refresh_data = {
        "refresh_token": refresh_token
    }

    response = await client.post(
        "/api/v1/auth/refresh",
        json=refresh_data
    )

    assert response.status_code == status.HTTP_200_OK
    new_tokens = response.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens
    assert new_tokens["access_token"] != tokens["access_token"]


@pytest.mark.asyncio
async def test_password_reset_request(client: AsyncClient, create_test_user):
    """Test password reset request"""
    reset_data = {
        "email": "auth_user@test.com"
    }

    response = await client.post(
        "/api/v1/auth/password-reset-request",
        json=reset_data
    )

    # Should return success even if email doesn't exist (security)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_validate_token(client: AsyncClient, create_test_user):
    """Test token validation endpoint"""
    # First login to get token
    login_data = {
        "username": "auth_user@test.com",
        "password": "auth_password123",
    }

    login_response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )

    tokens = login_response.json()
    access_token = tokens["access_token"]

    # Test the token validation endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post(
        "/api/v1/auth/validate-token",
        headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["is_valid"] is True


@pytest.mark.asyncio
async def test_logout(client: AsyncClient, create_test_user):
    """Test user logout functionality"""
    # First login to get token
    login_data = {
        "username": "auth_user@test.com",
        "password": "auth_password123",
    }

    login_response = await client.post(
        "/api/v1/auth/login",
        data=login_data
    )

    tokens = login_response.json()
    access_token = tokens["access_token"]

    # Test logout endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post(
        "/api/v1/auth/logout",
        headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
