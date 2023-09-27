import pytest
from app.main import app
from app.models.BoardGame import BoardGameId
from app.routers.boardgames import suggest_board_game
from fastapi.testclient import TestClient
from mongita import MongitaClientMemory

client = TestClient(app)


@pytest.mark.asyncio
async def test_mock_get_suggestions():
    client = MongitaClientMemory()
    boardGameId = BoardGameId(266192)
    await suggest_board_game(boardGameId, client)
    suggestions = client.boardgames.suggestions.find()

    assert all(["id" in bg for bg in suggestions])
    assert all(["name" in bg for bg in suggestions])
    assert all(["year" in bg for bg in suggestions])
    assert all(["count" in bg for bg in suggestions])

    client.close()
