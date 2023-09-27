from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_search_board_games():
    response = client.get("/api/boardgames/search/wingspan")
    assert response.status_code == 200
    results = response.json()

    assert all(["id" in bg for bg in results])
    assert all(["name" in bg for bg in results])
    assert all(["wingspan" in bg["name"].lower() for bg in results])
    assert all(["year" in bg for bg in results])
