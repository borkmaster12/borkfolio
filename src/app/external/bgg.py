from asyncio import sleep

import requests
from fastapi import HTTPException

from app.models.BggCollection import BggCollection
from app.models.BggSearchResultSet import BggSearchResultSet


async def get_my_collection() -> BggCollection:
    collection = None
    request = requests.get(
        "https://boardgamegeek.com/xmlapi2/collection?username=borkmeister&subtype=boardgame&own=1"
    )

    if request.status_code == 200:
        return BggCollection.from_xml(request.text)

    while request.status_code == 202 and collection is None:
        await sleep(4)
        collection = await get_my_collection()

    if collection:
        return collection
    else:
        raise HTTPException(request.status_code)


def search_board_games(query: str) -> BggSearchResultSet:
    query = query.replace(" ", "+")
    url = f"https://boardgamegeek.com/xmlapi2/search?query={query}&type=boardgame,boardgameexpansion"
    request = requests.get(url)

    if request.status_code == 200:
        return BggSearchResultSet.from_xml(request.text)

    raise HTTPException(request.status_code)
