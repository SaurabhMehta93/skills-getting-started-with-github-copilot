import copy

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dict before each test for isolation."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app_module.app, base_url="http://testserver") as ac:
        yield ac
