from pydantic import BaseModel, field_validator
from cpelib.types.product import Product
from cpelib.types.definitions import CPEPart


class CPE(BaseModel):
    part: CPEPart
    vendor: str
    product: str
    version: str = None
    update: str = None
    edition: str = None
    language: str = None
    sw_edition: str = None
    target_sw: str = None
    target_hw: str = None
    other: str = None

    @field_validator("part", mode="before")
    def parse_part(cls, value):
        return CPEPart(value)

    def get_product(self) -> Product:
        return Product(name=self.product, vendor=self.vendor, part=self.part)
