import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.config import settings
from tests.api.v1.base import BaseAPITest


class TestLocationAPI(BaseAPITest):
    """Test cases for Location API endpoints"""

    @pytest.mark.asyncio
    async def test_create_location(self, client: AsyncClient, superuser_token_headers: dict):
        """Test creating a new location (admin only)"""
        location_data = {
            "name": "Test City",
            "description": "A beautiful test city for tourism",
            "country": "Test Country",
            "region": "Test Region",
            "latitude": 10.123456,
            "longitude": 20.654321,
            "continent": "Asia",
            "is_active": True
        }

        # When: Creating a location with admin privileges
        response = await client.post(
            f"{settings.API_V1_STR}/locations/",
            headers=superuser_token_headers,
            json=location_data
        )

        # Then: Location should be created successfully
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == location_data["name"]
        assert data["country"] == location_data["country"]
        assert "id" in data

        # When: Attempting to create a location without admin privileges
        response = await client.post(
            f"{settings.API_V1_STR}/locations/",
            json=location_data
        )

        # Then: Request should be denied
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_read_locations(self, client: AsyncClient):
        """Test reading all locations (public endpoint)"""
        # When: Getting all locations
        response = await client.get(f"{settings.API_V1_STR}/locations/")

        # Then: Locations should be returned successfully
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_read_location(self, client: AsyncClient, superuser_token_headers: dict):
        """Test reading a specific location"""
        # First create a location
        location_data = {
            "name": "Read Test City",
            "description": "A city to test reading",
            "country": "Read Test Country",
            "region": "Read Test Region",
            "latitude": 11.123456,
            "longitude": 21.654321,
            "is_active": True
        }
        response = await client.post(
            f"{settings.API_V1_STR}/locations/",
            headers=superuser_token_headers,
            json=location_data
        )
        location_id = response.json()["id"]

        # When: Getting the location
        response = await client.get(f"{settings.API_V1_STR}/locations/{location_id}")

        # Then: Location details should be returned
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == location_id
        assert data["name"] == location_data["name"]

    @pytest.mark.asyncio
    async def test_update_location(self, client: AsyncClient, superuser_token_headers: dict):
        """Test updating a location"""
        # First create a location
        location_data = {
            "name": "Update Test City",
            "description": "A city to test updating",
            "country": "Update Test Country",
            "region": "Update Test Region",
            "latitude": 12.123456,
            "longitude": 22.654321,
            "is_active": True
        }
        response = await client.post(
            f"{settings.API_V1_STR}/locations/",
            headers=superuser_token_headers,
            json=location_data
        )
        location_id = response.json()["id"]

        # Update data
        update_data = {
            "name": "Updated City Name",
            "description": "Updated city description",
            "is_featured": True
        }

        # When: Updating the location with admin privileges
        response = await client.put(
            f"{settings.API_V1_STR}/locations/{location_id}",
            headers=superuser_token_headers,
            json=update_data
        )

        # Then: Location should be updated successfully
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == location_id
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
        assert data["is_featured"] == update_data["is_featured"]

    @pytest.mark.asyncio
    async def test_delete_location(self, client: AsyncClient, superuser_token_headers: dict):
        """Test deleting a location"""
        # First create a location
        location_data = {
            "name": "Delete Test City",
            "description": "A city to test deletion",
            "country": "Delete Test Country",
            "region": "Delete Test Region",
            "latitude": 13.123456,
            "longitude": 23.654321,
            "is_active": True
        }
        response = await client.post(
            f"{settings.API_V1_STR}/locations/",
            headers=superuser_token_headers,
            json=location_data
        )
        location_id = response.json()["id"]

        # When: Deleting the location with admin privileges
        response = await client.delete(
            f"{settings.API_V1_STR}/locations/{location_id}",
            headers=superuser_token_headers
        )

        # Then: Location should be deleted successfully
        assert response.status_code == status.HTTP_200_OK

        # Verify deletion
        response = await client.get(f"{settings.API_V1_STR}/locations/{location_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_get_locations_by_country(self, client: AsyncClient):
        """Test getting locations by country"""
        # When: Getting locations by country
        country = "Test Country"
        response = await client.get(
            f"{settings.API_V1_STR}/locations/country/{country}"
        )

        # Then: Locations for the specified country should be returned
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_locations_by_continent(self, client: AsyncClient):
        """Test getting locations by continent"""
        # When: Getting locations by continent
        continent = "Asia"
        response = await client.get(
            f"{settings.API_V1_STR}/locations/continent/{continent}"
        )

        # Then: Locations for the specified continent should be returned
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_featured_locations(self, client: AsyncClient):
        """Test getting featured locations"""
        # When: Getting featured locations
        response = await client.get(f"{settings.API_V1_STR}/locations/featured")

        # Then: Featured locations should be returned
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
