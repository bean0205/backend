import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.error_handling import AppException, ErrorCode


@pytest.mark.asyncio
async def test_app_exception_handler(client: AsyncClient):
    """Test that AppException is properly handled"""
    # The test client calls an endpoint that raises an AppException
    response = await client.get("/api/v1/test/error/app-exception")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "error" in data
    assert data["error"] == ErrorCode.BAD_REQUEST
    assert "message" in data
    assert "details" in data


@pytest.mark.asyncio
async def test_validation_exception(client: AsyncClient):
    """Test that validation errors are properly handled"""
    # Send invalid data to an endpoint
    response = await client.post(
        "/api/v1/users/",
        json={"email": "not-an-email", "password": "short"}  # Invalid data
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["error"] == "VALIDATION_ERROR"
    assert "details" in data
    assert "errors" in data["details"]


@pytest.mark.asyncio
async def test_not_found_exception(client: AsyncClient):
    """Test handling of resources not found"""
    # Try to access a non-existent resource
    response = await client.get("/api/v1/users/99999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["error"] == ErrorCode.NOT_FOUND


@pytest.mark.asyncio
async def test_unauthorized_exception(client: AsyncClient):
    """Test handling of unauthorized access"""
    # Try to access a protected endpoint without authentication
    response = await client.get("/api/v1/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["error"] == ErrorCode.UNAUTHORIZED
