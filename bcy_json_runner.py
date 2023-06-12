import os
import fire
from pathfinder.bcy import BcyWriter

def run(directory: str, output_file: str = "output.csv"):
    """
    Parse a single JSON file or all JSON files in a directory and save the data to a CSV file.
    :param directory: Path to the JSON file or directory
    :param output_file: Path to the output CSV file
    """
    # Instantiate the BcyWriter
    writer = BcyWriter(directory, output_file)

    # Parse the JSON files and save the results
    writer.parse_and_save()

if __name__ == "__main__":
    # python script_name.py --directory "path_to_directory" --output_file "output.csv"
    fire.Fire(run)
