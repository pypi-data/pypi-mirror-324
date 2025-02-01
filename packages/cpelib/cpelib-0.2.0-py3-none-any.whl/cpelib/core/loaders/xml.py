from tqdm import tqdm
from lxml import etree
from pathlib import Path
from typing import Iterator

from cpelib.types.item import CPEItem
from cpelib.types.generator import GeneratorInfo
from cpelib.core.loaders.base import BaseCPELoader


class XMLLoader(BaseCPELoader):
    def __init__(self, xml_file: str = '~/.cpelib/official-cpe-dictionary_v2.3.xml'):
        """
        Loader for CPE dictionary XML files. Parses the cpe-item elements in chunks.

        Args:
            xml_file (str): Path to the XML file.
        """

        # check if the file exists
        xml_file = Path(xml_file).expanduser()

        if not xml_file.exists():
            raise FileNotFoundError(f"File not found: {xml_file}")

        self.xml_file = xml_file
        self.generator_info = None

        self.context = etree.iterparse(self.xml_file, events=('start', 'end'))
        _, self.root = next(self.context)
        _, generator_element = next(self.context)

        # Read the first element after root - the <generator> node
        if generator_element is not None and generator_element.tag.endswith('generator'):
            self.generator_info = GeneratorInfo.from_xml(generator_element, self.root.nsmap)
            generator_element.clear()  # Clear generator from memory
        else:
            raise ValueError("Expected <generator> element as the first child of root.")

        print(self.generator_info)

    @property
    def nsmap(self) -> dict:
        """Returns the namespace map of the XML document."""
        return self.root.nsmap

    def __call__(self, *args, **kwargs) -> Iterator[CPEItem]:
        """
        Parses the XML file incrementally and yields CPE items.

        Yields:
            CPEItem: Parsed CPE item.
        """

        with tqdm(desc="Processing CPE items", unit="item") as pbar:
            # Process <cpe-item> elements
            for event, element in self.context:
                if event == 'end' and element.tag.endswith('cpe-item'):
                    # TODO: find cpe23-item with short version of namespace
                    cpe_item = CPEItem(
                        name=element.get('name'),
                        title=element.find('title', self.nsmap).text,
                        cpe=element.find('{http://scap.nist.gov/schema/cpe-extension/2.3}cpe23-item').get('name'),
                        deprecated=element.get('deprecated') == 'true',
                        deprecation_date={'deprecation_date': element.get('deprecation_date')},
                        references={'references': element.find('references', self.nsmap)}
                    )

                    yield cpe_item
                    element.clear()  # Clear the current cpe-item node from memory

                    # Free up memory for processed elements
                    while element.getprevious() is not None:
                        del element.getparent()[0]

                    pbar.update(1)
