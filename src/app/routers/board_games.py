from app.external.bgg import get_my_collection
from app.models.BggCollection import BggCollection
from fastapi import APIRouter

router = APIRouter()


@router.get("/api/boardgames", response_model=BggCollection, tags=["api"])
async def board_games() -> BggCollection:
    """Gets my collection of board games

    Data provided by BoardGameGeek

    Returns:
        BggCollection
    """
    return await get_my_collection()
