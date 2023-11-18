from pathlib import Path
from threading import Thread, Lock
from tqdm import tqdm
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from urllib.parse import urlparse, unquote

class URLDownloader:

    def __init__(self, show_tqdm:bool=True) -> None:
        # display tqdm progress bar for the list of URLs or not
        self.show_tqdm = show_tqdm

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
    def download_file(self, url: str, root_dir: str, tqdm_lock: Lock, pbar: tqdm) -> None:
        """Download a single file with retry logic."""
        try:
            # Extract the file name from the URL
            file_name = unquote(urlparse(url).path.split('/')[-1])
            target_path = Path(root_dir) / file_name
            target_path.parent.mkdir(parents=True, exist_ok=True)

            response = requests.get(url)
            if response.status_code == 200:
                with open(target_path, "wb") as f:
                    f.write(response.content)
                if self.show_tqdm:
                    with tqdm_lock:
                        pbar.update(1)
            else:
                print(f"🚨🚧🔥 Failed to download {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to download {url}. Exception: {e}")

    def download_files(self, file_urls: list[str], save_dir: str) -> None:
        """Download files from the given URLs into a local directory using threading."""
        threads = []
        tqdm_lock = Lock()

        with tqdm(total=len(file_urls), disable=not self.show_tqdm) as pbar:
            for file_url in file_urls:
                thread = Thread(target=self.download_file, args=(file_url, save_dir, tqdm_lock, pbar))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

if __name__ == '__main__':
    # Example usage
    downloader = URLDownloader()
    file_urls = ["https://sekai.best/asset_viewer/character/member/100001/100001_illust_1.png"]
    save_dir = r"E:\sekai\gatcha_card"
    downloader.download_files(file_urls, save_dir)
