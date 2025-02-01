from lxml import etree
from datetime import datetime
from pydantic import BaseModel

from cpelib.utils.common import XSD_DATETIME_FORMAT


class GeneratorInfo(BaseModel):
    product_name: str
    product_version: str
    schema_version: str
    timestamp: datetime

    @classmethod
    def from_xml(cls, element: etree._Element, nsmap: dict) -> "GeneratorInfo":
        """
            Parses the <generator> XML node into a GeneratorInfo object.
            :param element: The <generator> XML node.
            :param nsmap: The namespace map for the XML document.

            :return: GeneratorInfo
        """
        return cls(
            product_name=element.find("product_name", nsmap).text,
            product_version=element.find("product_version", nsmap).text,
            schema_version=element.find("schema_version", nsmap).text,
            timestamp=datetime.strptime(element.find("timestamp", nsmap).text, XSD_DATETIME_FORMAT)
        )

    def __str__(self):
        return f"{self.product_name} {self.product_version} - {self.schema_version} ({self.timestamp})"
