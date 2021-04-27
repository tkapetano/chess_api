import pytest
# pytest.fixture imports
from tests.test_helpers import client, get_test_db, create_test_database, URL, test_db_session as db

from sql_app.models import User


class TestUsers:
    def setup(self):
        self.users_url = "/users"

    @pytest.fixture(autouse=True)
    def setup_db_data(self, db):
        """Set up all the data before each test"""
        first_user = User(id=0, email="helloworld@testapi.com", hashed_password="password123")
        db.add(first_user)
        db.commit()
        db.refresh(first_user)

    def test_create_and_read_user(self, client):
        email = "kasparov@testthis.api"
        response = client.post(
            self.users_url + "/",
            json={"email": email, "password": "ilovechess123"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == email
        assert "id" in data
        user_id = data["id"]

        response = client.get(f"{self.users_url}/{user_id}")
        assert response.status_code == 200, response.text
        assert response.json() == {
            "email": email,
            "id": user_id,
            "is_active": True,
            "games": []
        }

    def test_read_non_exisiting_user(self, client):
        response = client.get(f"{self.users_url}/99999")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}
