from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst

import datetime
import re
import string
import urllib


class FirmwareLoader(ItemLoader):

    @staticmethod
    def find_product(text):
        match = re.search(r"(?:model[:. #]*([\w-][\w.-]+))", " ".join(
            text).replace(u"\xa0", " ").strip(), flags=re.IGNORECASE)
        return next((x for x in match.groups() if x), None) if match else None

    @staticmethod
    def find_version(text):
        match = re.search(r"(?:version[:. ]*([\w-][\w.-]+)|ve?r?s?i?o?n?[:. ]*([\d-][\w.-]+))",
                          " ".join(text).replace(u"\xa0", " ").strip(), flags=re.IGNORECASE)
        return next((x for x in match.groups() if x), None) if match else None

    @staticmethod
    def find_build(text):
        match = re.search(r"(?:build[:. ]*([\w-][\w.-]+)|bu?i?l?d?[:. ]*([\d-][\w.-]+))",
                          " ".join(text).replace(u"\xa0", " ").strip(), flags=re.IGNORECASE)
        return next((x for x in match.groups() if x), None) if match else None

    @staticmethod
    def find_version_period(text):
        match = re.search(r"((?:[0-9])(?:[\w-]*\.[\w-]*)+)",
                          " ".join(text).replace(u"\xa0", " ").strip())
        return next((x for x in match.groups() if x and "192.168." not in x.lower()), None) if match else None

    def clean(s):
        return "".join(filter(lambda x: x in string.printable, s)).replace("\r", "").replace("\n", "").replace(u"\xa0", " ").strip()

    def fix_url(url, loader_context):
        if not urllib.parse.urlparse(url).netloc:
            return urllib.parse.urljoin(loader_context.get("response").url, url)
        return url

    def remove_html(s):
        return re.sub(r"<[a-zA-Z0-9\"/=: ]+>", "", s)

    default_output_processor = TakeFirst()

    product_in = MapCompose(clean)
    vendor_in = Identity()

    description_in = MapCompose(remove_html, clean)
    version_in = MapCompose(clean)
    build_in = MapCompose(clean)

    mib_in = MapCompose(fix_url)
    sdk_in = MapCompose(fix_url)
    url_in = MapCompose(fix_url)
