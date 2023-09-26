from mongita import MongitaClientDisk

from app.external.bgg import get_my_collection

db_client = MongitaClientDisk(host="./.mongita")

db_bg_collection = db_client.boardgames.collection
db_bg_suggestions = db_client.boardgames.suggestions


async def refresh_collection() -> None:
    db_bg_collection.delete_many({})
    bgg_collection = (await get_my_collection()).collection
    db_bg_collection.insert_many([bg.dict() for bg in bgg_collection])


async def clear_suggestions() -> None:
    db_bg_suggestions.delete_many({})
