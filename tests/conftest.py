import pytest
from typing import AsyncGenerator

# Define common fixtures here that can be used across different test modules

@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    This is needed for pytest-asyncio.
    """
    import asyncio
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
