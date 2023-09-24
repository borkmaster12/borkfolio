from app.db import db_bg_collection, refresh_collection
from app.external.bgg import search_bgg_games
from app.models.BggSearch import BggSearchResultItem
from app.models.BoardGame import BoardGame
from fastapi import APIRouter

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
    await refresh_collection()

    return [bg for bg in db_bg_collection.find({})]


@router.post("/api/boardgames/search", response_model=list[BoardGame], tags=["api"])
async def search_board_games(name: str) -> list[BggSearchResultItem]:
    """Searches for board games using the provided query

    Data provided by BoardGameGeek

    Returns:
        List[BoardGame]
    """

    return search_bgg_games(name).boardGames
