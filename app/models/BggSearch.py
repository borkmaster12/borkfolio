from pydantic_xml import BaseXmlModel, attr, element, wrapped
from pydantic_xml.element.element import SearchMode


class BggSearchResultItem(BaseXmlModel, tag="item", search_mode=SearchMode.ORDERED):
    id: int = attr()
    name: str = wrapped("name", attr(name="value"))
    year: int | None = wrapped("yearpublished", attr(name="value"))
    minage: int | None = wrapped("minage", attr(name="value"))


class BggSearchResultSet(BaseXmlModel, tag="items"):
    total: int | None = attr()
    boardGames: list[BggSearchResultItem] | None = element(tag="item")
