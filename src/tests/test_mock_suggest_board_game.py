import pytest
from app.models.BoardGame import BoardGameId
from app.routers.boardgames import suggest_board_game
from mongita import MongitaClientMemory

@pytest.mark.asyncio
async def test_mock_suggest_board_game():
    client = MongitaClientMemory()
    boardGameId = BoardGameId(266192)
    suggestion = await suggest_board_game(boardGameId, client)

    assert suggestion["id"] == 266192
    assert suggestion["name"] == "Wingspan"
    assert suggestion["year"] == 2019
    assert suggestion["count"] == 1

    client.close()
