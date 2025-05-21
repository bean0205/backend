import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from app.crud.user import crud_user
from app.schemas.user import UserCreate, UserUpdate
from tests.crud.test_base import TestCRUDBase


class TestUserCRUD(TestCRUDBase):
    """Test cases for User CRUD operations"""

    @pytest.fixture
    async def crud_obj(self):
        return crud_user

    @pytest.fixture
    async def test_obj_data(self):
        return UserCreate(
            email="testuser@example.com",
            password="securepassword123",
            full_name="Test User",
            is_active=True
        )

    @pytest.fixture
    async def update_obj_data(self):
        return UserUpdate(
            full_name="Updated User Name",
            email="updated@example.com"
        )

    @pytest.mark.asyncio
    async def test_get_by_email(self, crud_obj, db_session, test_obj_data):
        """Test retrieving a user by email"""
        # Given: A created user
        user = await crud_obj.create(db_session, obj_in=test_obj_data)

        # When: Getting the user by email
        retrieved_user = await crud_obj.get_by_email(db_session, email=test_obj_data.email)

        # Then: The retrieved user should match the created one
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.email == test_obj_data.email

    @pytest.mark.asyncio
    async def test_authenticate(self, crud_obj, db_session, test_obj_data):
        """Test user authentication"""
        # Given: A created user
        user = await crud_obj.create(db_session, obj_in=test_obj_data)

        # When: Authenticating with correct credentials
        authenticated_user = await crud_obj.authenticate(
            db_session,
            email=test_obj_data.email,
            password=test_obj_data.password
        )

        # Then: Authentication should succeed
        assert authenticated_user is not None
        assert authenticated_user.id == user.id

        # When: Authenticating with incorrect password
        wrong_auth_user = await crud_obj.authenticate(
            db_session,
            email=test_obj_data.email,
            password="wrongpassword"
        )

        # Then: Authentication should fail
        assert wrong_auth_user is None

    @pytest.mark.asyncio
    async def test_is_superuser(self, crud_obj, db_session):
        """Test superuser verification"""
        # Given: A superuser and a regular user
        superuser_data = UserCreate(
            email="superuser@example.com",
            password="superpassword123",
            full_name="Super User",
            is_superuser=True
        )
        superuser = await crud_obj.create(db_session, obj_in=superuser_data)

        regular_user_data = UserCreate(
            email="regularuser@example.com",
            password="regularpassword123",
            full_name="Regular User",
            is_superuser=False
        )
        regular_user = await crud_obj.create(db_session, obj_in=regular_user_data)

        # When: Checking if users are superusers
        # Then: Results should match expected values
        assert crud_obj.is_superuser(superuser) is True
        assert crud_obj.is_superuser(regular_user) is False
