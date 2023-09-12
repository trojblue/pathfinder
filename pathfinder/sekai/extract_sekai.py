# Importing required libraries
from urllib.parse import urlencode
from xml.etree.ElementTree import fromstring
from pathlib import Path
from typing import List, Tuple
import requests
import os
from tqdm.auto import tqdm
from tenacity import retry, stop_after_attempt, wait_fixed
from threading import Thread, Lock


# Constants
BASE_URL = "https://storage.sekai.best/sekai-assets/"

# --- Network Operations ---


def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    response = requests.get(url)
    return (
        response.text
        if response.status_code == 200
        else f"Failed: {response.status_code}"
    )


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
    if namespace is None:
        namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    root = fromstring(xml_content)
    return [
        cp.find("s3:Prefix", namespace).text
        for cp in root.findall(".//s3:CommonPrefixes", namespace)
    ]


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


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def download_file(
    rel_path: str, url: str, root_dir: str, tqdm_lock: Lock, pbar: tqdm
) -> None:
    """Download a single file with retry logic."""
    target_path = Path(root_dir) / rel_path
    target_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url)
    if response.status_code == 200:
        with open(target_path, "wb") as f:
            f.write(response.content)
        with tqdm_lock:
            pbar.update(1)
    else:
        raise ConnectionError(
            f"Failed to download {url}. Status code: {response.status_code}"
        )


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


def scrape_by_prefix(prefix: str):
    """Scrape a single prefix. Assumes that no subdirectories exist."""
    url = generate_url(prefix)
    xml_content = fetch_url(url)
    extracted_file_urls = extract_file_urls(xml_content, BASE_URL)
    download_files_from_url_tup(extracted_file_urls, r"E:\sekai")
    print(f"Scraped {prefix}")


def scrape_by_prefixes(prefixes: List[str]):
    """Scrape multiple prefixes."""
    for prefix in tqdm(prefixes):
        scrape_by_prefix(prefix)


# --- Example usage ---


def scrape_driver():
    # reads a txt file containing prefixes in to a list
    with open(r"D:\CSC\pathfinder\_data_sync\sekai_voice_prefix_list.txt", "r") as f:
        prefixes = f.readlines()
    prefixes = [prefix.strip() for prefix in prefixes]
    scrape_by_prefixes(prefixes)


if __name__ == "__main__":
    # Uncomment this if you want to run the 'parse_xmls_to_prefix' function.
    # parse_xmls_to_prefix()

    scrape_driver()
