# Importing required libraries
from urllib.parse import urlencode
from xml.etree.ElementTree import fromstring, ParseError
from pathlib import Path
from typing import List, Tuple
import requests
import os
from tqdm.auto import tqdm
from tenacity import retry, stop_after_attempt, wait_fixed
from threading import Thread, Lock

import fire

# Constants
BASE_URL = "https://storage.sekai.best/sekai-assets/"


# --- Network Operations ---


def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Failed to fetch URL: {e}"


def generate_url(prefix: str, max_keys: int = 1000) -> str:
    """Generate an S3 URL with query parameters."""
    params = {
        "delimiter": "/",
        "list-type": 2,
        "max-keys": max_keys,
        "prefix": prefix,
    }
    return f"{BASE_URL}?{urlencode(params)}"


# --- XML Parsing ---


def parse_xml(xml_content: str, namespace=None) -> list:
    """Parse XML to extract 'CommonPrefixes'."""
    try:
        if namespace is None:
            namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
        root = fromstring(xml_content)
        return [
            cp.find("s3:Prefix", namespace).text
            for cp in root.findall(".//s3:CommonPrefixes", namespace)
        ]
    except ParseError as e:
        return [f"XML Parsing failed: {e}"]


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


# --- File Operations ---


@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def download_file(
    rel_path: str, url: str, root_dir: str, tqdm_lock: Lock, pbar: tqdm
) -> None:
    """Download a single file with retry logic."""
    try:
        target_path = Path(root_dir) / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)

        response = requests.get(url)
        if response.status_code == 200:
            with open(target_path, "wb") as f:
                f.write(response.content)
            with tqdm_lock:
                pbar.update(1)
        else:
            print(f"🚨🚧🔥 Failed to download {url}. Status code: {response.status_code}")
    except Exception as e:
        raise ConnectionError(f"Failed to download {url}. Exception: {e}")


def download_files_from_url_tup(
    url_tuples: List[Tuple[str, str]], root_dir: str
) -> None:
    """Download files from the given URLs into a local directory using threading."""

    threads = []
    tqdm_lock = Lock()

    with tqdm(total=len(url_tuples)) as pbar:
        for rel_path, url in url_tuples:
            thread = Thread(
                target=download_file, args=(rel_path, url, root_dir, tqdm_lock, pbar)
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()


# --- Main Functions ---


def scrape_prefixes(prefixes: List[str], save_dir: str):
    """Scrape multiple prefixes."""
    for prefix in tqdm(prefixes):
        try:
            url = generate_url(prefix)
            xml_content = fetch_url(url)
            extracted_file_urls = extract_file_urls(xml_content, BASE_URL)
            download_files_from_url_tup(extracted_file_urls, save_dir)
            print(f"Scraped {prefix}")
        except Exception as e:
            print(f"Failed to scrape prefix {prefix}. Exception: {e}")


# --- Example usage ---


def scrape_driver(todo_txt_path: str, save_dir: str = "./sekai"):
    # reads a txt file containing prefixes in to a list
    with open(todo_txt_path, "r") as f:
        prefixes = f.readlines()
    prefixes = [prefix.strip() for prefix in prefixes]
    scrape_prefixes(prefixes, save_dir)


if __name__ == "__main__":
    # todo_txt_path = r"D:\CSC\pathfinder\_data_sync\sekai_voice_prefix_list.txt"

    # python sekai_extract.py scrape_driver --todo_txt_path sekai_voice_prefix_list.txt --save_dir ./sekai
    fire.Fire(scrape_driver)
