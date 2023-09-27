from pydantic_xml import BaseXmlModel, attr, element, wrapped


class BggSearchResultItem(BaseXmlModel, tag="item", search_mode="ordered"):  # type: ignore
    id: int = attr()
    name: str = wrapped("name", attr(name="value"))
    year: int | None = wrapped("yearpublished", attr(name="value"))


class BggSearchResultSet(BaseXmlModel, tag="items"):
    total: int | None = attr()
    boardGames: list[BggSearchResultItem] | None = element(tag="item")
