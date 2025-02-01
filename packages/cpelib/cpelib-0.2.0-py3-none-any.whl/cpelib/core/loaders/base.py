from typing import Iterator
from abc import ABC, abstractmethod

from cpelib.types.item import CPEItem
from cpelib.types.dictionary import CPEDictionary


class BaseCPELoader(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Iterator[CPEItem]:
        """
            Lazily load CPE items.

            :param args:
            :param kwargs:

            :return:  Iterator[CPEItem]: Parsed CPE item.
        """
        raise NotImplementedError

    def load(self, **kwargs) -> CPEDictionary:
        """
        Eagerly loads CPE items.

        Returns:
            CPEDictionary: Dictionary of CPE items.
        """

        cpe_dict = CPEDictionary()

        for cpe_item in self(**kwargs):
            cpe_dict.add_item(cpe_item)

        return cpe_dict
