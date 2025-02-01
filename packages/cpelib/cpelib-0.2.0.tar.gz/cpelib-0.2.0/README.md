# cpelib
A Python package for parsing, representing, and filtering the NVD CPE Dictionary.


## Installation
```bash
pip install cpelib
```

## Setup
Before using the package, you need to download the NVD CPE Dictionary V2.3.
You can download the latest version from the NVD website: https://nvd.nist.gov/products/cpe

After downloading the file (e.g., `official-cpe-dictionary_v2.3.xml`), you can use the `cpelib` package to parse the 
file.

By default, the package looks for the file in the `~/.cpelib` directory.

```bash
mkdir ~/.cpelib
mv official-cpe-dictionary_v2.3.xml ~/.cpelib
```

Or, you can programmatically change the path by providing the path to the file in the `CPEDictionaryLoader` class.

```python
from cpelib.core.loader import CPEDictionaryLoader

loader = CPEDictionaryLoader(xml_file="path/to/official-cpe-dictionary_v2.3.xml")
```

## Usage
 
> [NOTE] It will take around 2 minutes to parse the entire XML file which contains over 1,341,950 CPE items.
> Also, makes sure you have enough memory to load the entire dictionary (16GB should be safe).

Use class CPEDictionaryLoader to define and initialize the loader, then call the loader to parse the XML file.
The loader will return a dictionary with the cpe-item entries.

```python
from cpelib.core.loader import CPEDictionaryLoader

loader = CPEDictionaryLoader()
cpe_dict = loader()
```

Additionally, you can explore the examples in the `examples` directory and run them using the following command:

```bash
python3 -m examples.load_cpe_dict
```
