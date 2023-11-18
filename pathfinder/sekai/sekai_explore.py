import os
from tqdm import tqdm
from pathfinder.sekai.sekai_extractor import *
from pathfinder.utils.file_downloader import URLDownloader


def extract_subfolder_prefixes(directory_path: str) -> list[str]:
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
    downloader = URLDownloader(show_tqdm=False)
    SAVE_ROOT_DIR = r"E:\sekai\gatcha_card"

    # get all sub-folders under character/member/
    prefix_list = extract_subfolder_prefixes("character/member/")

    for curr_prefix in tqdm(prefix_list, desc="Downloading gatcha card items"):
        curr_entries = extract_subfolder_prefixes(curr_prefix)
        file_urls = construct_file_urls(curr_entries, BASE_URL)

        # download files to ROOT_DIR/{last_folder_name} (eg. D:/res001_no001_rip)
        last_folder_name = curr_prefix.rstrip("/").split("/")[-1]
        curr_download_dir = os.path.join(SAVE_ROOT_DIR, last_folder_name)

        downloader.download_files(file_urls, curr_download_dir)


if __name__ == "__main__":
    gatcha_card_extract_driver()
