from typing import List, Tuple

import unibox
from tqdm.auto import tqdm
from pydub import AudioSegment
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


def extract_file_urls(
    xml_content: str, base_url: str, namespace=None
) -> List[Tuple[str, str]]:
    """Extract file URLs from given XML content."""
    if namespace is None:
        namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}

    root = fromstring(xml_content)
    file_keys = [
        content.find("s3:Key", namespace).text
        for content in root.findall(".//s3:Contents", namespace)
    ]
    return [(key, f"{base_url}/{key}") for key in file_keys]


# --- Main Functions ---


def scrape_prefixes(prefixes: List[str], save_dir: str):
    """Scrape multiple prefixes."""
    for prefix in tqdm(prefixes):
        try:
            url = generate_url(prefix)
            xml_content = fetch_url(url)
            extracted_file_urls = extract_file_urls(xml_content, BASE_URL)
            download_files_from_url(extracted_file_urls, save_dir)
            print(f"Scraped {prefix}")
        except Exception as e:
            print(f"Failed to scrape prefix {prefix}. Exception: {e}")


def scrape_driver(todo_txt_path: str, save_dir: str = "./sekai"):
    # reads a txt file containing prefixes in to a list
    with open(todo_txt_path, "r") as f:
        prefixes = f.readlines()
    prefixes = [prefix.strip() for prefix in prefixes]
    scrape_prefixes(prefixes, save_dir)


def explore_voice():
    URL = "sound/actionset/voice/"
    url = generate_url(URL)
    xml_content = fetch_url(url)
    extracted_file_urls = extract_file_urls(xml_content, BASE_URL)

    print(extracted_file_urls)


def calculate_total_audio_length(directory: str) -> float:
    """Calculate the total length of all mp3 files in the given directory."""
    total_length = 0.0  # Total length in seconds
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith('.mp3'):
            audio = AudioSegment.from_mp3(os.path.join(directory, filename))
            total_length += len(audio) / 1000.0  # Convert length to seconds
    print(f"Total length of audio in {directory}: {total_length} seconds")
    return total_length



if __name__ == "__main__":
    pass
    # parse_xmls_to_prefix()
    # parse_entry("event_story/")
