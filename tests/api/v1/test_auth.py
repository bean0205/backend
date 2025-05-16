import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.db.models import User


@pytest.fixture
async def test_user(test_db) -> User:
    """Create a test user"""
    async with AsyncSession(bind=test_db.bind) as session:
        test_user = User(
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("testpassword123"),
            is_active=True,
        )
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)
        return test_user


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    """Test user registration"""
    user_data = {
        "email": "newuser@example.com",
        "password": "securepassword123",
        "full_name": "New User"
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_existing_email(client: AsyncClient, test_user: User):
    """Test registration with existing email"""
    user_data = {
        "email": test_user.email,  # Use existing email
        "password": "securepassword123",
        "full_name": "Another User"
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 409
    assert "đã được sử dụng" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user: User):
    """Test user login"""
    login_data = {
        "username": test_user.email,
        "password": "testpassword123"
    }
    
    response = await client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == test_user.email


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user: User):
    """Test login with wrong password"""
    login_data = {
        "username": test_user.email,
        "password": "wrongpassword"
    }
    
    response = await client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_forgot_password(client: AsyncClient, test_user: User):
    """Test forgot password endpoint"""
    email_data = {
        "email": test_user.email
    }
    
    response = await client.post("/api/v1/auth/forgot-password", json=email_data)
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_reset_password_invalid_token(client: AsyncClient):
    """Test reset password with invalid token"""
    reset_data = {
        "token": "invalid_token",
        "new_password": "newpassword123"
    }
    
    response = await client.post("/api/v1/auth/reset-password", json=reset_data)
    assert response.status_code == 400
    assert "Token không hợp lệ" in response.json()["detail"]
