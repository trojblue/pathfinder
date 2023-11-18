import unibox
from pathfinder.sekai.sekai_extractor import *

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





if __name__ == "__main__":
    pass
    # parse_xmls_to_prefix()
    # parse_entry("event_story/")
