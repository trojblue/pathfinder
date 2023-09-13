from tqdm import tqdm
from pathfinder.sekai.sekai_extract import *
from pydub import AudioSegment
import os

def explore():
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
    # explore()
    calculate_total_audio_length(r"E:\sekai\kanade_audio_copy")
