from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_boardgames():
    response = client.get("/boardgames")
    assert response.status_code == 200
    assert "- Board Games" in response.text
