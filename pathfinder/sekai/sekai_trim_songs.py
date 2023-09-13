import os
from tqdm.auto import tqdm
from pydub import AudioSegment


def trim(source_dir, dest_dir):
    # Make sure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate through each file in the source directory
    for filename in tqdm(os.listdir(source_dir)):
        if filename.endswith(".flac"):
            # Load the FLAC file
            audio = AudioSegment.from_file(os.path.join(source_dir, filename), format="flac")

            # Cut off the first 7 seconds
            audio = audio[8950:]  # pydub works in milliseconds

            # Save the modified audio in the destination folder
            audio.export(os.path.join(dest_dir, filename), format="flac")

    print("Processing complete.")


if __name__ == '__main__':
    # Define the source and destination directories
    source_dir = r'E:\sekai\knd_songs'
    dest_dir = r'E:\sekai\knd_songs_converted'

    trim(source_dir, dest_dir)
