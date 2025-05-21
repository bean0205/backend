import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.accommodation import crud_accommodation
from app.schemas.accommodation import AccommodationCreate, AccommodationUpdate
from tests.crud.test_base import TestCRUDBase


class TestAccommodationCRUD(TestCRUDBase):
    """Test cases for Accommodation CRUD operations"""

    @pytest.fixture
    async def crud_obj(self):
        return crud_accommodation

    @pytest.fixture
    async def test_obj_data(self):
        return AccommodationCreate(
            name="Test Hotel",
            description="A luxurious test hotel",
            address="123 Test Street, Test City",
            price_range="$$$",
            location_id=1,  # Assumes a location with ID 1 exists
            amenities=["WiFi", "Pool", "Restaurant"],
            rating=4.5,
            is_active=True
        )

    @pytest.fixture
    async def update_obj_data(self):
        return AccommodationUpdate(
            name="Updated Hotel Name",
            description="Updated luxurious hotel description",
            price_range="$$$$",
            amenities=["WiFi", "Pool", "Restaurant", "Spa"]
        )

    @pytest.mark.asyncio
    async def test_get_by_location(self, crud_obj, db_session, test_obj_data):
        """Test retrieving accommodations by location ID"""
        # Given: A created accommodation
        accommodation = await crud_obj.create(db_session, obj_in=test_obj_data)

        # When: Getting accommodations by location ID
        accommodations = await crud_obj.get_by_location(
            db_session,
            location_id=test_obj_data.location_id
        )

        # Then: The retrieved accommodations should include the created one
        assert len(accommodations) >= 1
        assert any(acc.id == accommodation.id for acc in accommodations)

    @pytest.mark.asyncio
    async def test_get_by_price_range(self, crud_obj, db_session, test_obj_data):
        """Test retrieving accommodations by price range"""
        # Given: A created accommodation
        accommodation = await crud_obj.create(db_session, obj_in=test_obj_data)

        # When: Getting accommodations by price range
        accommodations = await crud_obj.get_by_price_range(
            db_session,
            price_range=test_obj_data.price_range
        )

        # Then: The retrieved accommodations should include the created one
        assert len(accommodations) >= 1
        assert any(acc.id == accommodation.id for acc in accommodations)

    @pytest.mark.asyncio
    async def test_get_by_amenities(self, crud_obj, db_session, test_obj_data):
        """Test retrieving accommodations by amenities"""
        # Given: A created accommodation
        accommodation = await crud_obj.create(db_session, obj_in=test_obj_data)

        # When: Getting accommodations by one of its amenities
        amenity = test_obj_data.amenities[0]
        accommodations = await crud_obj.get_by_amenities(
            db_session,
            amenities=[amenity]
        )

        # Then: The retrieved accommodations should include the created one
        assert len(accommodations) >= 1
        assert any(acc.id == accommodation.id for acc in accommodations)

    @pytest.mark.asyncio
    async def test_get_top_rated(self, crud_obj, db_session):
        """Test retrieving top-rated accommodations"""
        # Given: A high-rated accommodation
        high_rated_data = AccommodationCreate(
            name="Top Hotel",
            description="A top-rated test hotel",
            address="456 Top Street, Test City",
            price_range="$$$$",
            location_id=1,
            amenities=["WiFi", "Pool", "Restaurant", "Spa"],
            rating=5.0,
            is_active=True
        )
        high_rated = await crud_obj.create(db_session, obj_in=high_rated_data)

        # When: Getting top-rated accommodations (limit 5)
        top_accommodations = await crud_obj.get_top_rated(db_session, limit=5)

        # Then: The top-rated accommodations should include our high-rated one
        assert len(top_accommodations) >= 1
        assert any(acc.id == high_rated.id for acc in top_accommodations)
