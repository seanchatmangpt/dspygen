"""Test dspygen REST API."""

import httpx
from fastapi import Depends
from fastapi.testclient import TestClient

from dspygen.api import app, get_service_colony
from dspygen.rdddy.service_colony import ServiceColony

client = TestClient(app)


# def test_read_root(asys: ServiceColony = Depends(get_service_colony)) -> None:
#     """Test that reading the root is successful."""
#     response = client.get("/")
#     assert httpx.codes.is_success(response.status_code)
