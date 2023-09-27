from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_collection():
    response = client.get("/api/boardgames/mycollection")
    assert response.status_code == 200
    collection = response.json()
    assert all(["id" in bg for bg in collection])
    assert all(["name" in bg for bg in collection])
    assert all(["year" in bg for bg in collection])
