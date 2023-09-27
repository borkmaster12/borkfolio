from pydantic_xml import BaseXmlModel, attr, element


class BggCollectionItem(BaseXmlModel, tag="item"):
    id: int = attr(alias="objectid")
    name: str = element()
    year: int = element(tag="yearpublished")


class BggCollection(BaseXmlModel, tag="items"):
    total: int | None = attr(alias="totalitems")
    collection: list[BggCollectionItem] = element(tag="item")
