from asyncio import sleep

import requests
from app.models.BggCollection import BggCollection
from app.models.BggSearch import BggSearchResultItem, BggSearchResultSet
from fastapi import HTTPException


async def get_my_bgg_collection() -> BggCollection:
    collection = None
    request = requests.get(
        "https://boardgamegeek.com/xmlapi2/collection?username=borkmeister&subtype=boardgame&own=1"
    )

    if request.status_code == 200:
        return BggCollection.from_xml(request.content)

    while request.status_code == 202 and collection is None:
        await sleep(4)
        collection = await get_my_bgg_collection()

    if collection:
        return collection
    else:
        raise HTTPException(request.status_code)


def search_bgg_games(query: str) -> BggSearchResultSet:
    query = query.replace(" ", "+")
    url = f"https://boardgamegeek.com/xmlapi2/search?query={query}&type=boardgame,boardgameexpansion"
    response = requests.get(url)

    if response.status_code == 200:
        return BggSearchResultSet.from_xml(response.content)

    raise HTTPException(response.status_code)


def get_bgg_game_details(id: int) -> BggSearchResultItem | None:
    url = f"https://boardgamegeek.com/xmlapi2/thing?id={id}&type=boardgame,boardgameexpansion"
    response = requests.get(url)

    searchResult = BggSearchResultSet.from_xml(response.content)

    if searchResult.boardGames:
        return searchResult.boardGames[0]
    else:
        return None
