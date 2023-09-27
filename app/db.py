from mongita import MongitaClientDisk

from app.external.api_bgg import get_my_bgg_collection

db = MongitaClientDisk(host="./.mongita")


def get_db():
    return db


async def refresh_collection(db: MongitaClientDisk) -> None:
    collection = db.boardgames.collection
    collection.delete_many({})
    bgg_collection = (await get_my_bgg_collection()).collection
    collection.insert_many([bg.dict() for bg in bgg_collection])


async def clear_suggestions(db: MongitaClientDisk) -> None:
    collection = db.boardgames.suggestions
    collection.delete_many({})
