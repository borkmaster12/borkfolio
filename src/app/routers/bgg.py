from app.external.bgg_api import get_my_collection
from app.models.BggCollection import BggCollection
from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/myboardgames",
    response_model=BggCollection,
    description="Data provided by BoardGameGeek",
)
async def myboardgames() -> BggCollection:
    return get_my_collection()
