import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.config import settings
from tests.api.v1.base import BaseAPITest


class TestAccommodationAPI(BaseAPITest):
    """Test cases for Accommodation API endpoints"""

    @pytest.mark.asyncio
    async def test_create_accommodation(self, client: AsyncClient, superuser_token_headers: dict):
        """Test creating a new accommodation (admin only)"""
        # First, we need a location ID to associate with the accommodation
        location_data = {
            "name": "Accommodation Test City",
            "description": "City for testing accommodations",
            "country": "Test Country",
            "region": "Test Region",
            "latitude": 14.123456,
            "longitude": 24.654321,
            "is_active": True
        }
        response = await client.post(
            f"{settings.API_V1_STR}/locations/",
            headers=superuser_token_headers,
            json=location_data
        )
        location_id = response.json()["id"]

        # Now create an accommodation
        accommodation_data = {
            "name": "Test Hotel",
            "description": "A luxurious test hotel",
            "address": "123 Test Street, Test City",
            "price_range": "$$$",
            "location_id": location_id,
            "amenities": ["WiFi", "Pool", "Restaurant"],
            "rating": 4.5,
            "is_active": True
        }

        # When: Creating an accommodation with admin privileges
        response = await client.post(
            f"{settings.API_V1_STR}/accommodations/",
            headers=superuser_token_headers,
            json=accommodation_data
        )

        # Then: Accommodation should be created successfully
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == accommodation_data["name"]
        assert data["location_id"] == accommodation_data["location_id"]
        assert "id" in data

        # When: Attempting to create an accommodation without admin privileges
        response = await client.post(
            f"{settings.API_V1_STR}/accommodations/",
            json=accommodation_data
        )

        # Then: Request should be denied
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_read_accommodations(self, client: AsyncClient):
        """Test reading all accommodations (public endpoint)"""
        # When: Getting all accommodations
        response = await client.get(f"{settings.API_V1_STR}/accommodations/")

        # Then: Accommodations should be returned successfully
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_read_accommodation(self, client: AsyncClient, superuser_token_headers: dict):
        """Test reading a specific accommodation"""
        # First create a location and an accommodation
        location_data = {
            "name": "Read Accommodation Test City",
            "description": "City for testing accommodation reading",
            "country": "Test Country",
            "region": "Test Region",
            "latitude": 15.123456,
            "longitude": 25.654321,
            "is_active": True
        }
        response = await client.post(
            f"{settings.API_V1_STR}/locations/",
            headers=superuser_token_headers,
            json=location_data
        )
        location_id = response.json()["id"]

        accommodation_data = {
            "name": "Read Test Hotel",
            "description": "A hotel to test reading",
            "address": "456 Read Street, Test City",
            "price_range": "$$",
            "location_id": location_id,
            "amenities": ["WiFi", "Pool"],
            "rating": 4.0,
            "is_active": True
        }
        response = await client.post(
            f"{settings.API_V1_STR}/accommodations/",
            headers=superuser_token_headers,
            json=accommodation_data
        )
        accommodation_id = response.json()["id"]

        # When: Getting the accommodation
        response = await client.get(f"{settings.API_V1_STR}/accommodations/{accommodation_id}")

        # Then: Accommodation details should be returned
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == accommodation_id
        assert data["name"] == accommodation_data["name"]

    @pytest.mark.asyncio
    async def test_update_accommodation(self, client: AsyncClient, superuser_token_headers: dict):
        """Test updating an accommodation"""
        # First create a location and an accommodation
        location_data = {
            "name": "Update Accommodation Test City",
            "description": "City for testing accommodation updates",
            "country": "Test Country",
            "region": "Test Region",
            "latitude": 16.123456,
            "longitude": 26.654321,
            "is_active": True
        }
        response = await client.post(
            f"{settings.API_V1_STR}/locations/",
            headers=superuser_token_headers,
            json=location_data
        )
        location_id = response.json()["id"]

        accommodation_data = {
            "name": "Update Test Hotel",
            "description": "A hotel to test updates",
            "address": "789 Update Street, Test City",
            "price_range": "$$$",
            "location_id": location_id,
            "amenities": ["WiFi", "Pool"],
            "rating": 4.0,
            "is_active": True
        }
        response = await client.post(
            f"{settings.API_V1_STR}/accommodations/",
            headers=superuser_token_headers,
            json=accommodation_data
        )
        accommodation_id = response.json()["id"]

        # Update data
        update_data = {
            "name": "Updated Hotel Name",
            "description": "Updated luxury hotel description",
            "price_range": "$$$$",
            "amenities": ["WiFi", "Pool", "Restaurant", "Spa"]
        }

        # When: Updating the accommodation with admin privileges
        response = await client.put(
            f"{settings.API_V1_STR}/accommodations/{accommodation_id}",
            headers=superuser_token_headers,
            json=update_data
        )

        # Then: Accommodation should be updated successfully
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == accommodation_id
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
        assert data["price_range"] == update_data["price_range"]
        assert set(data["amenities"]) == set(update_data["amenities"])

    @pytest.mark.asyncio
    async def test_delete_accommodation(self, client: AsyncClient, superuser_token_headers: dict):
        """Test deleting an accommodation"""
        # First create a location and an accommodation
        location_data = {
            "name": "Delete Accommodation Test City",
            "description": "City for testing accommodation deletion",
            "country": "Test Country",
            "region": "Test Region",
            "latitude": 17.123456,
            "longitude": 27.654321,
            "is_active": True
        }
        response = await client.post(
            f"{settings.API_V1_STR}/locations/",
            headers=superuser_token_headers,
            json=location_data
        )
        location_id = response.json()["id"]

        accommodation_data = {
            "name": "Delete Test Hotel",
            "description": "A hotel to test deletion",
            "address": "101 Delete Street, Test City",
            "price_range": "$$",
            "location_id": location_id,
            "amenities": ["WiFi"],
            "rating": 3.5,
            "is_active": True
        }
        response = await client.post(
            f"{settings.API_V1_STR}/accommodations/",
            headers=superuser_token_headers,
            json=accommodation_data
        )
        accommodation_id = response.json()["id"]

        # When: Deleting the accommodation with admin privileges
        response = await client.delete(
            f"{settings.API_V1_STR}/accommodations/{accommodation_id}",
            headers=superuser_token_headers
        )

        # Then: Accommodation should be deleted successfully
        assert response.status_code == status.HTTP_200_OK

        # Verify deletion
        response = await client.get(f"{settings.API_V1_STR}/accommodations/{accommodation_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_get_accommodations_by_location(self, client: AsyncClient):
        """Test getting accommodations by location"""
        # When: Getting accommodations by location ID
        # (assumes location with ID 1 exists and has accommodations)
        location_id = 1
        response = await client.get(
            f"{settings.API_V1_STR}/accommodations/location/{location_id}"
        )

        # Then: Accommodations for the specified location should be returned
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_accommodations_by_price_range(self, client: AsyncClient):
        """Test getting accommodations by price range"""
        # When: Getting accommodations by price range
        price_range = "$$$"
        response = await client.get(
            f"{settings.API_V1_STR}/accommodations/price/{price_range}"
        )

        # Then: Accommodations for the specified price range should be returned
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_top_rated_accommodations(self, client: AsyncClient):
        """Test getting top-rated accommodations"""
        # When: Getting top-rated accommodations
        response = await client.get(f"{settings.API_V1_STR}/accommodations/top")

        # Then: Top-rated accommodations should be returned
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
