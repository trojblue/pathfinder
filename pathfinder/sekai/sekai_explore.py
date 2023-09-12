from pathfinder.sekai.extract_sekai import *


def explore():
    URL = "sound/actionset/voice/"
    url = generate_url(URL)
    xml_content = fetch_url(url)
    extracted_file_urls = extract_file_urls(xml_content, BASE_URL)

    print(extracted_file_urls)


if __name__ == "__main__":
    explore()
