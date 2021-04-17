from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sql_app.database import Base
from sql_app.sql_access import get_db
from main import api
from typing import Generator
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///tests/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


api.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db() -> Generator:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal()


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(api) as c:
        yield c


def test_create_and_read_user():
    email = "kasparov@testthis.api"
    response = client.post(
        "/users/",
        json={"email": email, "password": "ilovechess123"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == email
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "email": email,
        "id": user_id,
        "is_active": True,
        "games": []
    }


def test_read_non_exisiting_user():
    response = client.get("/users/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
