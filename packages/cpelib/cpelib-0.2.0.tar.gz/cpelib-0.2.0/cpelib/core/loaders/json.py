import json

from tqdm import tqdm
from glob import escape
from pathlib import Path
from typing import Iterator

from cpelib.types.item import CPEItem
from cpelib.core.loaders.base import BaseCPELoader


def load_from_file(file_path: Path) -> CPEItem | None:
    """
    Loads a CPE item from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        CPEItem: Parsed CPE item.
    """

    # check if the file exists
    expanded_file_path = Path(file_path).expanduser()

    if not expanded_file_path.exists():
        return None

    if not expanded_file_path.is_file():
        return None

    if expanded_file_path.suffix != '.json':
        return None

    with expanded_file_path.open(mode='r') as file:
        cpe_item_json = json.load(file)

    try:
        return CPEItem.parse_obj(cpe_item_json)
    except Exception as e:
        print(e)
        print(f"Error parsing {expanded_file_path}")
        return None


class JSONLoader(BaseCPELoader):
    def __init__(self, data_path: str = '~/.cpelib/data'):
        """
        Loader for CPE dictionary from JSON files.

        Args:
            data_path (str): Path to the directory containing JSON files.
        """

        # check if the file exists
        expanded_data_path = Path(data_path).expanduser()

        if not expanded_data_path.exists():
            raise FileNotFoundError(f"Directory not found: {expanded_data_path}")

        self.data_path = expanded_data_path

    def __call__(self, vendor_name: str = None, product_name: str = None) -> Iterator[CPEItem]:
        """
        Lazily load CPE items from the specified path.

        Args:
            vendor_name (str): Vendor name.
            product_name (str): Product name.

        Yields:
            CPEItem: Parsed CPE item.
        """

        search_string = ""

        if vendor_name:
            search_string += f"{escape(vendor_name)}"
        else:
            search_string += "*"

        if product_name:
            search_string += f"/{escape(product_name)}"
        else:
            search_string += "/*"

        search_string += "/*.json"

        files = self.data_path.rglob(search_string)
        progress_bar = tqdm(files, leave=False, desc="Loading CPE items")

        if not files:
            return Iterator()

        for json_file in progress_bar:
            cpe_item = load_from_file(json_file)

            if cpe_item is None:
                continue

            yield cpe_item
