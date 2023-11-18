from tqdm import tqdm
import unibox
from pathfinder.sekai.sekai_extractor import *
from pydub import AudioSegment
import os

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


def explore_4star_cards():
    URL = "character/member/"
    url = generate_url(URL)
    xml_content = fetch_url(url)
    extracted_file_urls = extract_file_urls(xml_content, BASE_URL)

    print("D")


def extract_subfolder_prefixes(directory_path:str) -> list[str]:
    """
    输入一个sekai站的相对路径, 返回所有下面的直接子文件夹的前缀
    Parse all XMLs in a directory into scrapable prefixes.
    :param entry_path: The path to the entry file. eg."sound/scenario/voice/"

    >>> prefixes = extract_subfolder_prefixes("event_story/")
    >>> print(prefixes[:3])
    ['event_story/100001/', 'event_story/100002/', 'event_story/100003/']
    """
    if directory_path.startswith("http"):
        raise ValueError("directory_path should be a relative path, not a url.")

    target_url = generate_url(directory_path)
    xml_data = fetch_url(target_url)
    subfolder_prefixes = parse_xml(xml_data)
    return subfolder_prefixes


def construct_file_urls(prefixes: list[str], base_url: str) -> list[str]:
    """
    Construct file URLs from a list of prefixes and a base URL.
    If a prefix ends with a '/', it's treated as a folder; otherwise, it's treated as a file.
    """
    return [f"{base_url}/{prefix}" for prefix in prefixes if not prefix.endswith('/')]


def gatcha_card_extract_driver():
    """
    从gatcha_card/中提取所有卡的前缀
    """
    prefix_list = extract_subfolder_prefixes("character/member/")

    for curr_prefix in prefix_list:
        curr_entries = extract_subfolder_prefixes(curr_prefix)
        file_urls = construct_file_urls(curr_entries, BASE_URL)

        # download somewhere
        # download_files_from_url_tup(file_urls, r"E:\sekai\gatcha_card")

        print("D")





if __name__ == "__main__":
    # explore_voice()
    # calculate_total_audio_length(r"E:\sekai\kanade_audio_copy")
    # explore_4star_cards()
    # extract_subfolder_prefixes("character/member/")
    gatcha_card_extract_driver()
