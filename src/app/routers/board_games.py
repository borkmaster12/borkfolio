from app.db import db_bg_collection, db_bg_suggestions
from app.external.api_bgg import get_bgg_game_details, search_bgg_games
from app.models.BggSearch import BggSearchResultItem
from app.models.BoardGame import BoardGame, BoardGameId, BoardGameSuggestion
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get(
    "/api/boardgames/mycollection", response_model=list[BoardGame], tags=["boardgames"]
)
async def get_my_board_games() -> list[BoardGame]:
    """Gets my collection of board games

    Data provided by BoardGameGeek

    Returns:
        List[BoardGame]
    """

    return [bg for bg in db_bg_collection.find({})]


@router.get(
    "/api/boardgames/search/{name}", response_model=list[BoardGame], tags=["boardgames"]
)
async def search_board_games(name: str) -> list[BggSearchResultItem]:
    """Searches for board games using the provided game name

    Data provided by BoardGameGeek

    Returns:
        List[BoardGame]
    """
    searchResult = search_bgg_games(name)

    if searchResult.boardGames:
        return searchResult.boardGames
    else:
        raise HTTPException(status_code=404, detail="No games found with that name")


@router.post(
    "/api/boardgames/suggestions",
    response_model=BoardGameSuggestion,
    tags=["boardgames"],
)
async def suggest_board_game(boardGameId: BoardGameId) -> dict:
    """Suggest a board game by providing its BoardGameGeek id

    Args:
        boardGameId (BoardGameId): The BoardGameGeek game id of the target game

    Raises:
        HTTPException: 404 - No game found with the provided id

    Returns:
        BoardGame
    """
    searchResult = get_bgg_game_details(boardGameId.value)

    if searchResult is None:
        raise HTTPException(status_code=404, detail="No game found with that id")

    suggestion = db_bg_suggestions.find_one({"id": boardGameId.value})

    if suggestion:
        db_bg_suggestions.update_one({"id": boardGameId.value}, {"$inc": {"count": 1}})
    else:
        suggestion = {**searchResult.dict(), "count": 1}
        db_bg_suggestions.insert_one(suggestion)

    return suggestion


@router.get(
    "/api/boardgames/suggestions",
    response_model=list[BoardGameSuggestion],
    tags=["boardgames"],
)
async def get_board_game_suggestions() -> list[BoardGameSuggestion]:
    """Get the current list of board game suggestions

    Returns:
        list[BoardGameRecommendation]: The current list of board game suggestions
    """
    suggestions = [bg for bg in db_bg_suggestions.find({})]
    return suggestions
