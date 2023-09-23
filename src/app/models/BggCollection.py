from app.models.BggCollectionItem import BggCollectionItem
from pydantic_xml import BaseXmlModel, attr, element


class BggCollection(BaseXmlModel, tag="items"):
    total: int | None = attr(alias="totalitems")
    collection: list[BggCollectionItem] = element(tag="item")
