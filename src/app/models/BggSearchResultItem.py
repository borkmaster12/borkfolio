from pydantic_xml import BaseXmlModel, attr, wrapped


class BggSearchResultItem(BaseXmlModel, tag="item"):
    id: int = attr()
    name: str = wrapped(
        "name",
        attr(name="value")
    )
    year: int = wrapped(
        "yearpublished", 
        attr(name="value")
    )
