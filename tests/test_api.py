"""Test dspygen REST API."""

import httpx
from fastapi import Depends
from fastapi.testclient import TestClient

from dspygen.api import app, get_actor_system
from dspygen.rdddy.actor_system import ActorSystem

client = TestClient(app)


# def test_read_root(asys: ActorSystem = Depends(get_actor_system)) -> None:
#     """Test that reading the root is successful."""
#     response = client.get("/")
#     assert httpx.codes.is_success(response.status_code)
