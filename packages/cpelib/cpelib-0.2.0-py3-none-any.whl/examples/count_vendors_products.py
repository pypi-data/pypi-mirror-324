from cpelib.core.loaders.xml import XMLLoader

loader = XMLLoader()

for item in loader():
    pass


vendors_count = 0
products_count = 0

for vendor in loader.dictionary.vendors.values():
    vendors_count += 1
    products_count += len(vendor)

print(f"Number of vendors: {vendors_count}")
print(f"Number of products: {products_count}")
