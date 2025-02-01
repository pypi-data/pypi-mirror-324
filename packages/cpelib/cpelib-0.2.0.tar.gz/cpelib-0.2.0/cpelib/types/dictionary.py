
from typing import Dict, List
from pydantic import BaseModel, Field

from cpelib.types.item import CPEItem
from cpelib.types.vendor import Vendor
from cpelib.types.reference import Reference


class CPEDictionary(BaseModel):
    items: Dict[str, CPEItem] = Field(default_factory=dict)
    vendors: Dict[str, Vendor] = Field(default_factory=dict)

    def __len__(self):
        return len(self.items)

    def add_item(self, cpe_item: CPEItem):
        """
            Adds a CPEItem and its vendor and product to the dictionary.

            Args:
                cpe_item (CPEItem): The CPE item to add.
        """

        self.items[cpe_item.name] = cpe_item

        vendor = self.vendors.get(cpe_item.cpe.vendor, None)

        if vendor is None:
            vendor = Vendor(name=cpe_item.cpe.vendor)
            self.vendors[vendor.name] = vendor

        if not vendor.has_product(cpe_item.cpe.product):
            product = cpe_item.cpe.get_product()
            vendor.add_product(product)

    def get_references(self) -> List[Reference]:
        """
            Returns all references in the dictionary.

            Returns:
                List[Reference]: List of references.
        """

        references = []

        for cpe_item in self.items.values():
            references.extend(cpe_item.references)

        return references
