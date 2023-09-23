from app.models.BggSearchResultItem import BggSearchResultItem
from pydantic_xml import BaseXmlModel, attr, element


class BggSearchResultSet(BaseXmlModel, tag="items"):
    total: int | None = attr()
    boardGames: list[BggSearchResultItem] = element(tag="item")
