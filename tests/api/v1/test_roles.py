import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, create_access_token
from app.db.models import User


@pytest.fixture
async def admin_user(test_db) -> User:
    """Create an admin test user"""
    async with AsyncSession(bind=test_db.bind) as session:
        admin_user = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=get_password_hash("adminpassword123"),
            is_active=True,
            role="admin",
            is_superuser=True,
        )
        session.add(admin_user)
        await session.commit()
        await session.refresh(admin_user)
        return admin_user


@pytest.fixture
async def regular_user(test_db) -> User:
    """Create a regular test user"""
    async with AsyncSession(bind=test_db.bind) as session:
        regular_user = User(
            email="user@example.com",
            full_name="Regular User",
            hashed_password=get_password_hash("userpassword123"),
            is_active=True,
            role="user",
        )
        session.add(regular_user)
        await session.commit()
        await session.refresh(regular_user)
        return regular_user


async def get_admin_token_headers(admin_user: User) -> dict:
    """Get admin token headers"""
    access_token = create_access_token(subject=admin_user.id)
    return {"Authorization": f"Bearer {access_token}"}


async def get_user_token_headers(regular_user: User) -> dict:
    """Get user token headers"""
    access_token = create_access_token(subject=regular_user.id)
    return {"Authorization": f"Bearer {access_token}"}


@pytest.mark.asyncio
async def test_create_location_admin(
    client: AsyncClient, admin_user: User
):
    """Test creating a location as admin"""
    headers = await get_admin_token_headers(admin_user)
    location_data = {
        "name": "Admin Test Location",
        "description": "Created by admin",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "address": "Test Address",
        "city": "New York",
        "country": "USA",
    }
    
    response = await client.post(
        "/api/v1/locations/", 
        json=location_data,
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == location_data["name"]


@pytest.mark.asyncio
async def test_create_location_regular_user(
    client: AsyncClient, regular_user: User
):
    """Test that regular users cannot create locations"""
    headers = await get_user_token_headers(regular_user)
    location_data = {
        "name": "User Test Location",
        "description": "Created by regular user",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "address": "Test Address",
        "city": "New York",
        "country": "USA",
    }
    
    response = await client.post(
        "/api/v1/locations/", 
        json=location_data,
        headers=headers
    )
    # Should return 403 Forbidden
    assert response.status_code == 403
    assert "Không đủ quyền hạn" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_users_admin(
    client: AsyncClient, admin_user: User
):
    """Test that admins can access user list"""
    headers = await get_admin_token_headers(admin_user)
    
    response = await client.get(
        "/api/v1/users/",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_users_regular_user(
    client: AsyncClient, regular_user: User
):
    """Test that regular users cannot access user list"""
    headers = await get_user_token_headers(regular_user)
    
    response = await client.get(
        "/api/v1/users/",
        headers=headers
    )
    # Should return 403 Forbidden
    assert response.status_code == 403
