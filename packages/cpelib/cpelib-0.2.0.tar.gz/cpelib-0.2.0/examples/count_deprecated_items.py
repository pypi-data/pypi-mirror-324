from cpelib.core.loaders.xml import XMLLoader

loader = XMLLoader()

deprecated_count = 0

for cpe_item in loader():
    if cpe_item.deprecated:
        deprecated_count += 1

print(f"Number of deprecated items: {deprecated_count}")
