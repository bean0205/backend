import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status

from app.main import app


class BaseAPITest:
    """Base class for API endpoint tests"""

    @pytest_asyncio.fixture
    async def client(self, setup_database):
        """Create an async HTTP client for testing API endpoints"""
        async with setup_database() as session:
            async with AsyncClient(app=app, base_url="http://test") as client:
                yield client

    @pytest_asyncio.fixture
    async def superuser_token_headers(self, client):
        """Get superuser token headers for authentication"""
        login_data = {
            "username": "admin@example.com",
            "password": "admin"
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        token = response.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}

    @pytest_asyncio.fixture
    async def normal_user_token_headers(self, client):
        """Get normal user token headers for authentication"""
        login_data = {
            "username": "user@example.com",
            "password": "password"
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        token = response.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}
