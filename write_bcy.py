import fire
import os
from pathlib import Path
from pathfinder.bcy import BcyWriter

def run(in_dir: str, out_dir:str=None, use_parquet: bool = True):
    """
    Parse a single JSON file or all JSON files in a directory and save the data to a CSV file.
    :param in_dir: Path to the JSON file, or directory containing jsons
    :param out_dir: Path to the folder where the output file will be saved (<in_dir>.parquet or <in_dir>.csv)
    :param use_parquet: 是否保存为parquet文件
    """

    dir_name = Path(in_dir).name
    suffix = ".parquet" if use_parquet else ".csv"
    out_dir = out_dir or ""
    out_file = os.path.join(out_dir, dir_name + suffix)

    # Instantiate the BcyWriter
    writer = BcyWriter(in_dir, out_file)

    # Parse the JSON files and save the results
    writer.parse_and_save(use_parquet=use_parquet)

if __name__ == "__main__":
    # python script_name.py --directory "path_to_directory" --output_file "output.csv"
    fire.Fire(run)
