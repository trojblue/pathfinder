import time
import requests
import jsonlines
import tempfile
import base64
from getpass import getpass
import collections

class DanbooruArtistFinder:
    def __init__(self):
        self.base_url = "https://danbooru.donmai.us"
        self.jsonl_file = tempfile.NamedTemporaryFile(delete=False).name
        self.found_artists = {}  # Now a dictionary
        self.username = "trojblue"
        self.api_key = "GxxdkUzfJhdr5btsiCcLbMNT"

    def find_artists(self, url: str, page_limit: int = 10):
        with jsonlines.open(self.jsonl_file, mode='a') as writer:
            if url in self.found_artists:
                return self.found_artists

            auth_str = f"{self.username}:{self.api_key}"
            auth_b64 = base64.b64encode(auth_str.encode()).decode()

            headers = {
                "Authorization": f"Basic {auth_b64}"
            }

            artist_counter = collections.Counter()

            for page in range(1, page_limit + 1):
                search_url = f"{self.base_url}/posts.json?tags=source%3A{url}&limit=200&page={page}"
                response = requests.get(search_url, headers=headers)
                data = response.json()
                print(data)

                for post in data:
                    tags = post["tag_string_artist"].split(" ")
                    artist_counter.update(tags)

                time.sleep(2)

            most_common_artists = [artist for artist, _ in artist_counter.most_common(2)]

            if most_common_artists:
                self.found_artists[url] = most_common_artists
                writer.write({"url_handle": url, "danbooru_key": most_common_artists, "not_found": False})
            else:
                writer.write({"url_handle": url, "danbooru_key": "", "not_found": True})
                print(f"{url}: not found")

            return self.found_artists


def local_test(url):
    finder = DanbooruArtistFinder()
    artists = finder.find_artists(url)
    return artists


if __name__ == "__main__":
    url = "https://twitter.com/miya_ki00"  # replace with the url you want to test with
    print(local_test(url))
