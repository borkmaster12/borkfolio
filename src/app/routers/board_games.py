from app.db import db_bg_collection, refresh_collection
from app.models.BoardGame import BoardGame
from fastapi import APIRouter

router = APIRouter()


@router.get("/api/boardgames", response_model=list[BoardGame], tags=["api"])
async def board_games() -> list[BoardGame]:
    """Gets my collection of board games

    Data provided by BoardGameGeek

    Returns:
        List[BoardGame]
    """
    await refresh_collection()

    return [bg for bg in db_bg_collection.find({})]
