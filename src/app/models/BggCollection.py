from app.models.BggCollectionItem import BggCollectionItem
from pydantic_xml import BaseXmlModel, attr, element


class BggCollection(BaseXmlModel, tag="items"):
    totalItems: int | None = attr(alias="totalitems")
    boardGames: list[BggCollectionItem] = element(tag="item")
