import os
import requests
from tqdm import tqdm
from urllib.parse import urlencode
from xml.etree.ElementTree import fromstring, ParseError
from pathfinder.utils.file_downloader import URLDownloader  # Replace with actual module name

class SekaiAssetExtractor:
    BASE_URL = "https://storage.sekai.best/sekai-assets/"

    def __init__(self, root_dir: str):
        self.downloader = URLDownloader(show_tqdm=False)
        self.root_dir = root_dir

    def fetch_url(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def generate_url(self, prefix: str, max_keys: int = 1000) -> str:
        params = {"delimiter": "/", "list-type": 2, "max-keys": max_keys, "prefix": prefix}
        return f"{self.BASE_URL}?{urlencode(params)}"

    def parse_xml(self, xml_content: str, namespace=None) -> list:
        if namespace is None:
            namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
        root = fromstring(xml_content)
        common_prefixes = [cp.find("s3:Prefix", namespace).text for cp in root.findall(".//s3:CommonPrefixes", namespace)]
        return common_prefixes if common_prefixes else [contents.find("s3:Key", namespace).text for contents in root.findall(".//s3:Contents", namespace)]

    def extract_and_download(self, prefix: str):
        target_url = self.generate_url(prefix)
        xml_data = self.fetch_url(target_url)
        entries = self.parse_xml(xml_data)

        if entries and entries[0].endswith('/'):
            for entry in tqdm(entries, desc=f"Processing {prefix}", unit="entry"):
                self.extract_and_download(entry)
        else:
            file_urls = [f"{self.BASE_URL}/{entry}" for entry in entries]
            save_dir = os.path.join(self.root_dir, *prefix.split('/')[:-1])
            self.downloader.download_files(file_urls, save_dir)


    def run_extraction(self, initial_prefix: str):
        print(f"Starting extraction for: {initial_prefix}")
        self.extract_and_download(initial_prefix)
        print("Extraction complete.")

if __name__ == '__main__':
    # Usage
    extractor = SekaiAssetExtractor(r"E:\sekai\gatcha_card")
    extractor.run_extraction("character/member/")
