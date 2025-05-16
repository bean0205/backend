import pytest
from typing import AsyncGenerator, Generator

import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.db.session import get_db
from app.core.config import settings
from app.db.models import Base


# Test database URL - use a different database for testing
TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    "/travel", "/travel_test"
)

# Create test engine and session
engine_test = create_async_engine(
    TEST_DATABASE_URL, 
    echo=False,
    poolclass=NullPool,
)
async_session_test = sessionmaker(
    engine_test, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False, 
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    This is needed for pytest-asyncio.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def setup_database() -> AsyncGenerator:
    """
    Create all tables in the test database and yield,
    then drop all tables after tests are done.
    """
    # Create tables
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # Run the tests
    
    # Drop tables
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db(setup_database) -> AsyncGenerator:
    """
    Yield a database session for each test, then roll back after the test is done.
    """
    async with async_session_test() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest.fixture
async def client(db) -> AsyncGenerator:
    """
    Yield a test client with a database session dependency override.
    """
    # Override the database dependency with our test database
    async def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create a test client using the app
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # Clear the dependency override after the test
    app.dependency_overrides.clear()
