from cpelib.core.loaders.json import JSONLoader

loader = JSONLoader()
cve_dict = loader.load(vendor_name="apple", product_name="iphone_os")

references = cve_dict.get_references()

print(len(references))
