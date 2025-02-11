import os
import requests
from lxml import etree


class ECFRAPI:
    def __init__(self, api_base_url: str, cache_dir: str):
        self.api_base_url = api_base_url
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_agencies(self):
        response = requests.get(f"{self.api_base_url}/api/admin/v1/agencies.json")
        return response.json()["agencies"]

    def get_titles(self):
        response = requests.get(f"{self.api_base_url}/api/versioner/v1/titles.json")
        return response.json()["titles"]

    def get_xml(
        self,
        date: str,
        title_id: int,
        subtitle: str = None,
        chapter: str = None,
        subchapter: str = None,
        part: str = None,
        subpart: str = None,
        section: str = None,
    ):

        # NOTE: This endpoint (api/versioner/v1/full/{date}/title-{title_id}.xml) should return a subset of a
        # title's XML based on the lowest leaf node given. I couldn't get it to work. When I passed a title and
        # chapter it still returned the entire title. So instead, I'm downloading/caching the entire title and
        # using XPaths to filter down to the specific subtitle/chapter/part/subpart/section requested.

        # Get the full XML for the given date and title from the cache. If it doesn't exist, download it.
        cache_file = os.path.join(self.cache_dir, f"{date}-title-{title_id}.xml")
        if not os.path.exists(cache_file):
            response = requests.get(
                f"{self.api_base_url}/api/versioner/v1/full/{date}/title-{title_id}.xml"
            )
            with open(cache_file, "w") as f:
                f.write(response.text)
        xml = etree.parse(cache_file)

        # Use XPaths to find the specific subtitle/chapter/part being requested.
        # The nodes look something like this: <DIV{n} N="IV" TYPE="CHAPTER">...</DIV{n}>
        def find_xml_node(value, type_value):
            result = xml.xpath(
                f".//*[starts-with(name(), 'DIV')][@N='{value}'][@TYPE='{type_value}']"
            )
            if len(result) == 0:
                raise Exception(
                    f"Unable to locate {type_value} {value} in the XML for title {title_id}"
                )
            return result[0]

        # Check each level in the hierarchy for the requested value.
        if subtitle is not None:
            xml = find_xml_node(subtitle, "SUBTITLE")
        if chapter is not None:
            xml = find_xml_node(chapter, "CHAPTER")
        if subchapter is not None:
            xml = find_xml_node(subchapter, "SUBCHAP")
        if part is not None:
            xml = find_xml_node(part, "PART")
        if subpart is not None:
            xml = find_xml_node(subpart, "SUBPART")
        if section is not None:
            xml = find_xml_node(section, "SECTION")

        return xml
