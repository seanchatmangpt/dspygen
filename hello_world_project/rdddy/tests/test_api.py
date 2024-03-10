"""Test rdddy REST API."""

import httpx
from fastapi.testclient import TestClient

from rdddy.api import app

client = TestClient(app)


def test_read_root() -> None:
    """Test that reading the root is successful."""
    response = client.get("/")
    assert httpx.codes.is_success(response.status_code)
