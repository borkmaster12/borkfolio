from pydantic_xml import BaseXmlModel, attr, element


class BggCollectionItem(BaseXmlModel, tag="item"):
    id: int = attr(alias="objectid")
    name: str = element()
    year: int = element(tag="yearpublished")
