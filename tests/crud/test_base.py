import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.crud.base import CRUDBase
from app.db.models import Base


@pytest.mark.asyncio
class TestCRUDBase:
    """Base class for testing CRUD operations"""

    @pytest_asyncio.fixture
    async def crud_obj(self):
        """Override in subclasses to provide the specific CRUD object to test"""
        raise NotImplementedError("Subclasses must implement this")

    @pytest_asyncio.fixture
    async def db_session(self, setup_database):
        """Get a clean database session for testing"""
        async with setup_database() as session:
            yield session

    @pytest_asyncio.fixture
    async def test_obj_data(self):
        """Override in subclasses to provide test data for creating objects"""
        raise NotImplementedError("Subclasses must implement this")

    @pytest_asyncio.fixture
    async def update_obj_data(self):
        """Override in subclasses to provide data for updating objects"""
        raise NotImplementedError("Subclasses must implement this")

    async def test_create(self, crud_obj, db_session, test_obj_data):
        """Test creating a new object"""
        # When: Creating a new object
        obj = await crud_obj.create(db_session, obj_in=test_obj_data)

        # Then: The object should be created with provided data
        assert obj.id is not None
        for key, value in test_obj_data.dict().items():
            # Skip None values and relationships which may be loaded lazily
            if value is not None and not key.endswith("_id") and not key.endswith("s"):
                assert getattr(obj, key) == value

        return obj

    async def test_get(self, crud_obj, db_session, test_obj_data):
        """Test getting an object by ID"""
        # Given: A created object
        created_obj = await self.test_create(crud_obj, db_session, test_obj_data)

        # When: Getting the object by ID
        retrieved_obj = await crud_obj.get(db_session, id=created_obj.id)

        # Then: The retrieved object should match the created one
        assert retrieved_obj is not None
        assert retrieved_obj.id == created_obj.id

    async def test_get_multi(self, crud_obj, db_session, test_obj_data):
        """Test retrieving multiple objects"""
        # Given: Multiple created objects
        obj1 = await crud_obj.create(db_session, obj_in=test_obj_data)
        obj2 = await crud_obj.create(db_session, obj_in=test_obj_data)

        # When: Getting multiple objects
        objects = await crud_obj.get_multi(db_session)

        # Then: The retrieved objects should include created ones
        assert len(objects) >= 2
        assert any(obj.id == obj1.id for obj in objects)
        assert any(obj.id == obj2.id for obj in objects)

    async def test_update(self, crud_obj, db_session, test_obj_data, update_obj_data):
        """Test updating an object"""
        # Given: A created object
        created_obj = await self.test_create(crud_obj, db_session, test_obj_data)

        # When: Updating the object
        updated_obj = await crud_obj.update(db_session, db_obj=created_obj, obj_in=update_obj_data)

        # Then: The updated object should have new values
        assert updated_obj.id == created_obj.id
        for key, value in update_obj_data.dict().items():
            if value is not None and not key.endswith("_id") and not key.endswith("s"):
                assert getattr(updated_obj, key) == value

    async def test_remove(self, crud_obj, db_session, test_obj_data):
        """Test removing an object"""
        # Given: A created object
        created_obj = await self.test_create(crud_obj, db_session, test_obj_data)
        obj_id = created_obj.id

        # When: Removing the object
        removed_obj = await crud_obj.remove(db_session, id=obj_id)

        # Then: The object should be removed
        assert removed_obj.id == obj_id

        # And: The object should no longer exist in the database
        retrieved_obj = await crud_obj.get(db_session, id=obj_id)
        assert retrieved_obj is None
