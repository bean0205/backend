import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.config import settings
from tests.api.v1.base import BaseAPITest


class TestUserAPI(BaseAPITest):
    """Test cases for User API endpoints"""

    @pytest.mark.asyncio
    async def test_create_user(self, client: AsyncClient, superuser_token_headers: dict):
        """Test creating a new user (admin only)"""
        user_data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "full_name": "New User"
        }

        # When: Creating a user with admin privileges
        response = await client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=user_data
        )

        # Then: User should be created successfully
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data

        # When: Creating a user without admin privileges
        response = await client.post(
            f"{settings.API_V1_STR}/users/",
            json=user_data
        )

        # Then: Request should be denied
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_read_users(self, client: AsyncClient, superuser_token_headers: dict):
        """Test reading all users (admin only)"""
        # When: Getting all users with admin privileges
        response = await client.get(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers
        )

        # Then: Users should be returned successfully
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # When: Getting all users without admin privileges
        response = await client.get(f"{settings.API_V1_STR}/users/")

        # Then: Request should be denied
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_read_user(self, client: AsyncClient, superuser_token_headers: dict):
        """Test reading a specific user"""
        # First create a user
        user_data = {
            "email": "testread@example.com",
            "password": "password123",
            "full_name": "Test Read User"
        }
        response = await client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=user_data
        )
        user_id = response.json()["id"]

        # When: Getting the user with admin privileges
        response = await client.get(
            f"{settings.API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers
        )

        # Then: User details should be returned
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == user_data["email"]

    @pytest.mark.asyncio
    async def test_update_user(self, client: AsyncClient, superuser_token_headers: dict):
        """Test updating a user"""
        # First create a user
        user_data = {
            "email": "updateuser@example.com",
            "password": "password123",
            "full_name": "Update Test User"
        }
        response = await client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=user_data
        )
        user_id = response.json()["id"]

        # Update data
        update_data = {
            "full_name": "Updated User Name",
            "email": "updated@example.com"
        }

        # When: Updating the user with admin privileges
        response = await client.put(
            f"{settings.API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers,
            json=update_data
        )

        # Then: User should be updated successfully
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["full_name"] == update_data["full_name"]
        assert data["email"] == update_data["email"]

    @pytest.mark.asyncio
    async def test_delete_user(self, client: AsyncClient, superuser_token_headers: dict):
        """Test deleting a user"""
        # First create a user
        user_data = {
            "email": "deleteuser@example.com",
            "password": "password123",
            "full_name": "Delete Test User"
        }
        response = await client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=user_data
        )
        user_id = response.json()["id"]

        # When: Deleting the user with admin privileges
        response = await client.delete(
            f"{settings.API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers
        )

        # Then: User should be deleted successfully
        assert response.status_code == status.HTTP_200_OK

        # Verify deletion
        response = await client.get(
            f"{settings.API_V1_STR}/users/{user_id}",
            headers=superuser_token_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_read_user_me(self, client: AsyncClient, normal_user_token_headers: dict):
        """Test reading the current user's data"""
        # When: Getting the current user data with user token
        response = await client.get(
            f"{settings.API_V1_STR}/users/me",
            headers=normal_user_token_headers
        )

        # Then: Current user details should be returned
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "full_name" in data

    @pytest.mark.asyncio
    async def test_update_user_me(self, client: AsyncClient, normal_user_token_headers: dict):
        """Test updating the current user's data"""
        # Update data
        update_data = {
            "full_name": "Updated My Name"
        }

        # When: Updating the current user data with user token
        response = await client.put(
            f"{settings.API_V1_STR}/users/me",
            headers=normal_user_token_headers,
            json=update_data
        )

        # Then: Current user should be updated successfully
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
