import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.config import settings
from tests.api.v1.base import BaseAPITest


class TestAuthAPI(BaseAPITest):
    """Test cases for Authentication API endpoints"""

    @pytest.mark.asyncio
    async def test_login(self, client: AsyncClient):
        """Test user login"""
        # When: Logging in with valid credentials
        login_data = {
            "username": "user@example.com",
            "password": "password"
        }
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            json=login_data
        )

        # Then: Login should succeed and return a token
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

        # When: Logging in with invalid credentials
        invalid_login = {
            "username": "user@example.com",
            "password": "wrongpassword"
        }
        response = await client.post(
            f"{settings.API_V1_STR}/auth/login",
            json=invalid_login
        )

        # Then: Login should fail
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_signup(self, client: AsyncClient):
        """Test user signup"""
        # When: Registering a new user
        signup_data = {
            "email": "newsignup@example.com",
            "password": "strongpassword123",
            "full_name": "New Signup User"
        }
        response = await client.post(
            f"{settings.API_V1_STR}/auth/signup",
            json=signup_data
        )

        # Then: Registration should succeed
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == signup_data["email"]
        assert data["full_name"] == signup_data["full_name"]
        assert "id" in data

        # When: Registering with an existing email
        response = await client.post(
            f"{settings.API_V1_STR}/auth/signup",
            json=signup_data
        )

        # Then: Registration should fail
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_password_reset_request(self, client: AsyncClient):
        """Test password reset request"""
        # When: Requesting password reset for existing email
        reset_data = {
            "email": "user@example.com"
        }
        response = await client.post(
            f"{settings.API_V1_STR}/auth/password-reset",
            json=reset_data
        )

        # Then: Request should be accepted
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_verify_token(self, client: AsyncClient, normal_user_token_headers: dict):
        """Test token verification"""
        # When: Verifying a valid token
        response = await client.get(
            f"{settings.API_V1_STR}/auth/verify",
            headers=normal_user_token_headers
        )

        # Then: Verification should succeed
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "email" in data
        assert "user_id" in data

        # When: Verifying an invalid token
        response = await client.get(
            f"{settings.API_V1_STR}/auth/verify",
            headers={"Authorization": "Bearer invalid_token"}
        )

        # Then: Verification should fail
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
