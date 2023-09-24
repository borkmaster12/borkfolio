from datetime import datetime, timedelta

from mongita import MongitaClientDisk

from app.external.bgg import get_my_collection

db_client = MongitaClientDisk(host="./.mongita")

db_bg_collection = db_client.boardgames.collection
db_last_bg_collection_update = db_client.boardgames.lastupdate


async def refresh_collection() -> None:
    last_update_doc = db_last_bg_collection_update.find_one() or {}

    should_refresh = bool(
        not last_update_doc
        or datetime.utcnow() > last_update_doc["time"] + timedelta(days=1),
    )

    if should_refresh:
        bgg_collection = (await get_my_collection()).collection
        db_bg_collection.insert_many([bg.dict() for bg in bgg_collection])
        if not last_update_doc:
            db_last_bg_collection_update.insert_one({"time": datetime.utcnow()})
        else:
            db_last_bg_collection_update.update_one(
                {}, {"$set": {"time": datetime.utcnow()}}
            )
