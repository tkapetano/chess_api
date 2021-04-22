import pytest

from tests.test_helpers import client, get_test_db, create_test_database, URL, test_db_session as db

class TestApps:
    def setup(self):
        self.application_url = "/applications"

    @pytest.fixture(autouse=True)
    def setup_db_data(self, db):
        """Set up all the data before each test"""
        new_app = AppModel(**APP)
        db.add(new_app)
        db.commit()
        db.refresh(new_app)

    def test_404(self, client, db):
        response = client.get("/applications")
        assert response.status_code == 200

    def test_create_and_read_user(self, client):
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

    def test_read_non_exisiting_user(self, client):
        response = client.get("/users/99999")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}
