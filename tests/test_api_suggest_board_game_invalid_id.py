from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_suggest_board_game_invalid_id():
    response = client.post(
        url="/api/boardgames/suggestions",
        json={"value": -1},
    )
    assert response.status_code == 404
