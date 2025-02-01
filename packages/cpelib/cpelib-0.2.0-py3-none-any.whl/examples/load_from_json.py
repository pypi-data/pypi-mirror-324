from cpelib.core.loaders.json import JSONLoader

loader = JSONLoader()
cve_dict = loader.load(vendor_name="microsoft")

print(len(cve_dict))
