import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_request_id_middleware(client: AsyncClient):
    """Test that the RequestLoggerMiddleware adds a request ID to responses"""
    response = await client.get("/api/v1/health")

    assert response.status_code == status.HTTP_200_OK
    assert "X-Request-ID" in response.headers
    assert "X-Process-Time" in response.headers


@pytest.mark.asyncio
async def test_security_headers_middleware(client: AsyncClient):
    """Test that the SecurityHeadersMiddleware adds security headers to responses"""
    response = await client.get("/api/v1/health")

    assert response.status_code == status.HTTP_200_OK
    assert "X-Content-Type-Options" in response.headers
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "X-Frame-Options" in response.headers
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Strict-Transport-Security" in response.headers
    assert "X-XSS-Protection" in response.headers
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
