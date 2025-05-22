import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app import crud
from app.schemas.role import RoleCreate, RoleUpdate


@pytest.fixture
async def create_test_admin_user(db: AsyncSession):
    """Create a superuser for testing protected endpoints"""
    from app.schemas.user import UserCreate
    from app.db.models import User

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
async def create_test_role(db: AsyncSession):
    """Create a test role"""
    role_data = RoleCreate(
        name="Test Role",
        description="Role for testing",
        permissions=[1, 2]  # Assuming these permission IDs exist
    )
    role = await crud.role.create(db, obj_in=role_data)
    return role


@pytest.mark.asyncio
async def test_create_role(client: AsyncClient, admin_token_headers, db: AsyncSession):
    """Test creating a new role"""
    role_data = {
        "name": "Editor Role",
        "description": "Editor role for testing",
        "permissions": [1, 2]
    }

    response = await client.post(
        "/api/v1/roles/",
        headers=admin_token_headers,
        json=role_data
    )

    assert response.status_code == status.HTTP_200_OK
    created_role = response.json()
    assert created_role["name"] == "Editor Role"
    assert created_role["description"] == "Editor role for testing"
    assert len(created_role["permissions"]) == 2


@pytest.mark.asyncio
async def test_create_role_existing_name(
        client: AsyncClient, admin_token_headers, db: AsyncSession, create_test_role
):
    """Test creating a role with existing name (should fail)"""
    role_data = {
        "name": "Test Role",  # Same name as fixture
        "description": "Another test role",
        "permissions": [1]
    }

    response = await client.post(
        "/api/v1/roles/",
        headers=admin_token_headers,
        json=role_data
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_read_roles(client: AsyncClient, admin_token_headers, create_test_role):
    """Test retrieving all roles"""
    response = await client.get(
        "/api/v1/roles/",
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    roles = response.json()
    assert len(roles) >= 1
    assert any(role["name"] == "Test Role" for role in roles)


@pytest.mark.asyncio
async def test_read_role(client: AsyncClient, admin_token_headers, create_test_role):
    """Test retrieving a role by ID"""
    role_id = create_test_role.id

    response = await client.get(
        f"/api/v1/roles/{role_id}",
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    role = response.json()
    assert role["id"] == role_id
    assert role["name"] == "Test Role"
    assert role["description"] == "Role for testing"


@pytest.mark.asyncio
async def test_read_role_not_found(client: AsyncClient, admin_token_headers):
    """Test retrieving a non-existent role"""
    response = await client.get(
        "/api/v1/roles/999999",  # Non-existent ID
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_role(client: AsyncClient, admin_token_headers, create_test_role):
    """Test updating a role"""
    role_id = create_test_role.id
    update_data = {
        "name": "Updated Test Role",
        "description": "Updated description",
        "permissions": [1, 2, 3]
    }

    response = await client.put(
        f"/api/v1/roles/{role_id}",
        headers=admin_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_200_OK
    updated_role = response.json()
    assert updated_role["name"] == "Updated Test Role"
    assert updated_role["description"] == "Updated description"
    assert len(updated_role["permissions"]) == 3


@pytest.mark.asyncio
async def test_update_role_not_found(client: AsyncClient, admin_token_headers):
    """Test updating a non-existent role"""
    update_data = {
        "name": "New Role Name",
        "description": "New description"
    }

    response = await client.put(
        "/api/v1/roles/999999",  # Non-existent ID
        headers=admin_token_headers,
        json=update_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_role(client: AsyncClient, admin_token_headers, create_test_role):
    """Test deleting a role"""
    role_id = create_test_role.id

    response = await client.delete(
        f"/api/v1/roles/{role_id}",
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_200_OK

    # Verify role no longer exists
    get_response = await client.get(
        f"/api/v1/roles/{role_id}",
        headers=admin_token_headers
    )

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test accessing roles endpoints without authentication"""
    response = await client.get("/api/v1/roles/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = await client.post("/api/v1/roles/", json={"name": "Unauthorized Role"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
