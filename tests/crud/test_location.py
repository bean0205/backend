import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.location import crud_location
from app.schemas.location import LocationCreate, LocationUpdate
from tests.crud.test_base import TestCRUDBase


class TestLocationCRUD(TestCRUDBase):
    """Test cases for Location CRUD operations"""

    @pytest.fixture
    async def crud_obj(self):
        return crud_location

    @pytest.fixture
    async def test_obj_data(self):
        return LocationCreate(
            name="Test City",
            description="A beautiful test city for tourism",
            country="Test Country",
            region="Test Region",
            latitude=10.123456,
            longitude=20.654321,
            continent="Asia",
            is_active=True
        )

    @pytest.fixture
    async def update_obj_data(self):
        return LocationUpdate(
            name="Updated City Name",
            description="Updated description for this location",
            is_featured=True
        )

    @pytest.mark.asyncio
    async def test_get_by_name(self, crud_obj, db_session, test_obj_data):
        """Test retrieving a location by name"""
        # Given: A created location
        location = await crud_obj.create(db_session, obj_in=test_obj_data)

        # When: Getting the location by name
        retrieved_location = await crud_obj.get_by_name(db_session, name=test_obj_data.name)

        # Then: The retrieved location should match the created one
        assert retrieved_location is not None
        assert retrieved_location.id == location.id
        assert retrieved_location.name == test_obj_data.name

    @pytest.mark.asyncio
    async def test_get_by_country(self, crud_obj, db_session, test_obj_data):
        """Test retrieving locations by country"""
        # Given: A created location
        location = await crud_obj.create(db_session, obj_in=test_obj_data)

        # When: Getting locations by country
        locations = await crud_obj.get_by_country(db_session, country=test_obj_data.country)

        # Then: The retrieved locations should include the created one
        assert len(locations) >= 1
        assert any(loc.id == location.id for loc in locations)

    @pytest.mark.asyncio
    async def test_get_by_continent(self, crud_obj, db_session, test_obj_data):
        """Test retrieving locations by continent"""
        # Given: A created location
        location = await crud_obj.create(db_session, obj_in=test_obj_data)

        # When: Getting locations by continent
        locations = await crud_obj.get_by_continent(db_session, continent=test_obj_data.continent)

        # Then: The retrieved locations should include the created one
        assert len(locations) >= 1
        assert any(loc.id == location.id for loc in locations)

    @pytest.mark.asyncio
    async def test_get_featured(self, crud_obj, db_session):
        """Test retrieving featured locations"""
        # Given: A featured location
        featured_location_data = LocationCreate(
            name="Featured City",
            description="A featured tourist destination",
            country="Featured Country",
            region="Featured Region",
            latitude=30.123456,
            longitude=40.654321,
            is_featured=True,
            is_active=True
        )
        featured_location = await crud_obj.create(db_session, obj_in=featured_location_data)

        # When: Getting featured locations
        featured_locations = await crud_obj.get_featured(db_session)

        # Then: The list should include our featured location
        assert len(featured_locations) >= 1
        assert any(loc.id == featured_location.id for loc in featured_locations)
