import pytest
# pytest.fixture imports
from tests.test_helpers import client, get_test_db, create_test_database, URL, test_db_session as db

from sql_app.models import User, Game


class TestGames:
    def setup(self):
        self.games_url = "/games"

    @pytest.fixture(autouse=True)
    def setup_db_data(self, db):
        """Set up all the data before each test"""
        first_user = User(id=42, email="helloworld@testapi.com", hashed_password="password123")
        first_game = Game(id=0, title='WhoKnows', owner_id=42)
        db.add_all([first_user, first_game])
        db.commit()
        db.refresh(first_user)

    def test_read_existing_games(self, client):
        response = client.get(f"{self.games_url}/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        first_game = data[0]
        assert first_game["id"] == 0
        assert first_game["owner_id"] == 42

    def test_create_and_read_game(self, client):
        user_id = 42
        response = client.post(
            f"/users/{user_id}/games/",
            json={"title": "testGames"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["owner_id"] == user_id
        assert "id" in data
        game_id = data["id"]

        response = client.get(f"/users/{user_id}/games/")
        #response = client.get(f"/users/{user_id}/{game_id}/",)
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        game = data[1]
        assert game["id"] == game_id
        assert game["owner_id"] == user_id
