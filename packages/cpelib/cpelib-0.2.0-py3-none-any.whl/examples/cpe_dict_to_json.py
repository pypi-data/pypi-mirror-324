import json

from glob import escape
from pathlib import Path
from cpelib.core.loaders.xml import XMLLoader

loader = XMLLoader()

output_path = Path(f"~/.cpelib/data").expanduser()
output_path.mkdir(parents=True, exist_ok=True)


for cpe_item in loader():
    if cpe_item.deprecated:
        continue

    # clean_vendor = cpe_item.cpe.vendor.replace("\\", "").replace("/", "")

    vendor_path = output_path / escape(cpe_item.cpe.vendor)
    vendor_path.mkdir(parents=True, exist_ok=True)

    # clean_product = cpe_item.cpe.product.replace("\\", "").replace("/", "")

    product_path = vendor_path / escape(cpe_item.cpe.product)
    product_path.mkdir(parents=True, exist_ok=True)

    version_components = cpe_item.name.replace("::", "").split(":")[4:]
    version_ref = "_".join(version_components)
    clean_name = (version_ref.replace("\\", "").replace("/", "").replace(".", "_")
                  .replace("-", "_").replace("~", "_").replace("%", "_"))

    json_file = product_path / f"{clean_name}.json"

    cpe_item_dict = cpe_item.model_dump()
    # CPEPart is not JSON serializable
    cpe_item_dict["cpe"]["part"] = cpe_item_dict["cpe"]["part"].value

    with json_file.open(mode="w") as f:
        json.dump(cpe_item_dict, f, indent=2)
