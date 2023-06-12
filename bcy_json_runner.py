import os
import fire
import csv
from tqdm.auto import tqdm
from pathfinder.bcy import BcyJsonParser


def transform_json(json_file: str):
    """
    Transform a single BCY JSON file into a dict
    """
    parser = BcyJsonParser()
    res = parser.parse_json(json_file)
    return res


def transform_directory_jsons(directory_path: str):
    """
    Transform all BCY JSON files in a directory into a dict
    """
    parser = BcyJsonParser()

    # Final dict to hold all the data
    combined_dict = {}

    # List all files in the directory
    pbar = tqdm(os.listdir(directory_path))
    for filename in pbar:
        # Only process files ending with .json
        pbar.set_description(f"Processing {filename}")
        if filename.endswith(".json"):
            json_file = os.path.join(directory_path, filename)

            # Parse each JSON file and update the combined_dict
            res = parser.parse_json(json_file)
            combined_dict.update(res)

    # Return the combined data
    return combined_dict


def save_dict_to_csv(data_dict: dict, output_file: str):
    # Open the file in write mode
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        # If the dictionary is not empty
        if data_dict:
            # Write the header (keys of the first item)
            header = ["date_rank"] + list(next(iter(data_dict.values())).keys())
            writer = csv.DictWriter(csvfile, fieldnames=header)

            writer.writeheader()
            # Write each row
            for date_rank, row in data_dict.items():
                # Add the date_rank to each row dict
                row["date_rank"] = date_rank
                writer.writerow(row)


def do_parse_json(json_path: str, output_path: str = "output.csv"):
    """
    Parse a single JSON file and save it to a CSV file
    :param json_path: Path to the JSON file, or directory
    :param output_path: Path to the output CSV file
    """
    # if is a file
    if os.path.isfile(json_path):
        j = transform_json(json_path)
    # if is a directory
    elif os.path.isdir(json_path):
        j = transform_directory_jsons(json_path)
    else:
        raise ValueError(f"Invalid path: {json_path}")

    # Save the parsed data to a CSV file
    print(f"Saving to {output_path}")
    save_dict_to_csv(j, output_path)
    print("Done")


if __name__ == "__main__":
    fire.Fire(do_parse_json)
