import unibox
from pathfinder.sekai.sekai_extract import *

"""
输入相对路径 eg."event_story" -> https://sekai.best/asset_viewer/event_story/
输出所有可爬取的前缀, 保存到txt
"""


def parse_xmls_to_prefix():
    """Parse all XMLs in a directory into scrapable prefixes."""
    xml_paths = unibox.traverses(r"D:\CSC\pathfinder\DATA\sekai")
    prefix_list = []

    for xml_path in xml_paths:
        xml_content = open(xml_path, "r", encoding="utf-8").read()
        common_prefixes = parse_xml(xml_content)
        prefix_list.extend(common_prefixes)

    prefix_list = list(set(prefix_list))
    prefix_list.sort()
    unibox.saves(prefix_list, r"sekai_voice_prefix_list.txt")


def parse_entry(entry_path):
    """Parse all XMLs in a directory into scrapable prefixes.
    :param entry_path: The path to the entry file. eg."sound/scenario/voice/"
    """
    url = generate_url(entry_path)
    xml_content = fetch_url(url)
    common_prefixes = parse_xml(xml_content)

    unibox.saves(common_prefixes, f"{entry_path.replace('/', '_')}_prefix_list.txt")
    print(common_prefixes)


if __name__ == "__main__":
    # parse_xmls_to_prefix()
    parse_entry("event_story/")
