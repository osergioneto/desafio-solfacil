from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.tests.crud.db.session import TestingSessionLocal
from app.main import app

@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()

@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c