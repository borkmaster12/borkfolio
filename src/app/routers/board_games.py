from app.db import db_bg_collection, db_bg_suggestions, refresh_collection
from app.external.bgg import search_bgg_game, search_bgg_games
from app.models.BggSearch import BggSearchResultItem
from app.models.BoardGame import BoardGame, BoardGameId
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get(
    "/api/boardgames/mycollection", response_model=list[BoardGame], tags=["api"]
)
async def get_my_board_games() -> list[BoardGame]:
    """Gets my collection of board games

    Data provided by BoardGameGeek

    Returns:
        List[BoardGame]
    """

    return [bg for bg in db_bg_collection.find({})]


@router.get(
    "/api/boardgames/search/{name}", response_model=list[BoardGame], tags=["api"]
)
async def search_board_games(name: str) -> list[BggSearchResultItem]:
    """Searches for board games using the provided query

    Data provided by BoardGameGeek

    Returns:
        List[BoardGame]
    """
    searchResult = search_bgg_games(name)

    if searchResult.boardGames:
        return searchResult.boardGames
    else:
        raise HTTPException(status_code=404, detail="No games found with that name")


@router.post("/api/boardgames/suggestions", response_model=BoardGame, tags=["api"])
async def suggest_board_game(boardGameId: BoardGameId) -> BggSearchResultItem:
    searchResult = search_bgg_game(boardGameId.id)

    if searchResult is None:
        raise HTTPException(status_code=404, detail="No game found with that id")

    db_bg_suggestions.insert_one(searchResult.dict())
    return searchResult


@router.get("/api/boardgames/suggestions", response_model=list[BoardGame], tags=["api"])
async def get_board_game_suggestions() -> list[BoardGame]:
    return [bg for bg in db_bg_suggestions.find({})]
