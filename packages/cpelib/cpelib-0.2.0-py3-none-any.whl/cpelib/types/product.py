from pydantic import BaseModel
from cpelib.types.definitions import CPEPart


class Product(BaseModel):
    name: str
    vendor: str
    part: CPEPart

    def equals(self, other):
        return self.name == other.name and self.vendor == other.vendor and self.part == other.part

    def __hash__(self):
        return hash((self.name, self.vendor, self.part))

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False

        return self.equals(other)

    def __str__(self):
        return f"{self.vendor} {self.name} {self.part.value}"
