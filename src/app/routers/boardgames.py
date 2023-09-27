from app.db import get_db
from app.external.api_bgg import get_bgg_game_details, search_bgg_games
from app.models.BggSearch import BggSearchResultItem
from app.models.BoardGame import BoardGame, BoardGameId, BoardGameSuggestion
from fastapi import APIRouter, Depends, HTTPException
from mongita import MongitaClientDisk

router = APIRouter(prefix="/api/boardgames")


@router.get("/mycollection", response_model=list[BoardGame], tags=["boardgames"])
async def get_my_board_games(
    db: MongitaClientDisk = Depends(get_db),
) -> list[BoardGame]:
    """Gets my collection of board games.

    Data provided by BoardGameGeek

    Returns:
        List[BoardGame]
    """

    return [bg for bg in db.boardgames.collection.find({})]


@router.get("/search/{name}", response_model=list[BoardGame], tags=["boardgames"])
async def search_board_games(name: str) -> list[BggSearchResultItem]:
    """Searches for board games using the provided game name.

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
    "/suggestions",
    response_model=BoardGameSuggestion,
    tags=["boardgames"],
)
async def suggest_board_game(
    boardGameId: BoardGameId,
    db: MongitaClientDisk = Depends(get_db),
) -> dict:
    """Suggest a board game by providing its BoardGameGeek id.

    Args:
        boardGameId (BoardGameId): The BoardGameGeek id of the target game

    Raises:
        HTTPException: 404 - No game found with the provided id

    Returns:
        BoardGame
    """
    suggestions = db.boardgames.suggestions
    searchResult = get_bgg_game_details(boardGameId.value)

    if searchResult is None:
        raise HTTPException(
            status_code=404, detail=f"No game found with id {boardGameId.value}"
        )

    suggestion = suggestions.find_one({"id": boardGameId.value})

    if suggestion:
        suggestions.update_one({"id": boardGameId.value}, {"$inc": {"count": 1}})
        suggestion["count"] += 1
    else:
        suggestion = {**searchResult.dict(), "count": 1}
        suggestions.insert_one(suggestion)

    return suggestion


@router.get(
    "/suggestions",
    response_model=list[BoardGameSuggestion],
    tags=["boardgames"],
)
async def get_board_game_suggestions(
    db: MongitaClientDisk = Depends(get_db),
) -> list[BoardGameSuggestion]:
    """Get the current list of board game suggestions.

    Returns:
        List[BoardGameRecommendation]
    """
    suggestions = [bg for bg in db.boardgames.suggestions.find({})]
    return suggestions
