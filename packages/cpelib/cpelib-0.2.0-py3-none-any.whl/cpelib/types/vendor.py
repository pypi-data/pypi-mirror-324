from pydantic import BaseModel, Field
from typing import Dict
from cpelib.types.product import Product


class Vendor(BaseModel):
    name: str
    products: Dict[str, Product] = Field(default_factory=dict)

    def has_product(self, name: str):
        return name in self.products

    def add_product(self, product: Product):
        self.products[product.name] = product

    def __len__(self):
        return len(self.products)

    def __str__(self):
        return self.name

    def __hash__(self):
        # TODO: probably should hash products as well
        return hash(self.name)

    def __eq__(self, other):
        # TODO: probably should compare products as well
        if not isinstance(other, Vendor):
            return False

        return self.name == other.name
