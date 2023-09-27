from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_about():
    response = client.get("/about")
    assert response.status_code == 200
    assert "About Site" in response.text
