import os
import csv
import logging
from typing import Dict, Union
from tqdm import tqdm
from pathfinder.bcy import BcyJsonParser

class BcyWriter:
    def __init__(self, directory: str, output_file: str):
        self.directory = directory
        self.output_file = output_file
        self.parser = BcyJsonParser()

    def transform_json(self, json_file: str) -> Dict[str, Union[str, int, float]]:
        return self.parser.parse_json(json_file)

    def transform_directory_jsons(self) -> Dict[str, Dict[str, Union[str, int, float]]]:
        if not os.path.isdir(self.directory):
            raise ValueError(f"Invalid directory path: {self.directory}")

        combined_dict = {}
        pbar = tqdm(os.listdir(self.directory))
        for filename in pbar:
            pbar.set_description(f"Processing {filename}")
            if filename.endswith(".json"):
                json_file = os.path.join(self.directory, filename)
                res = self.parser.parse_json(json_file)
                combined_dict.update(res)
        return combined_dict

    @staticmethod
    def _sanitize(value: str) -> str:
        return ''.join(char for char in value if char.isprintable())

    def save_dict_to_csv(self, data_dict: Dict[str, Dict[str, Union[str, int, float]]]):
        if not data_dict:
            logging.warning("Data dictionary is empty. Skipping CSV creation.")
            return
        with open(self.output_file, "w", newline="", encoding="utf-8") as csvfile:
            header = ["date_rank"] + list(next(iter(data_dict.values())).keys())
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            for date_rank, row in data_dict.items():
                sanitized_row = {k: self._sanitize(str(v)) for k, v in row.items()}
                sanitized_row["date_rank"] = date_rank
                writer.writerow(sanitized_row)

    def parse_and_save(self):
        if os.path.isfile(self.directory):
            data_dict = self.transform_json(self.directory)
        else:
            data_dict = self.transform_directory_jsons()
        logging.info(f"Saving to {self.output_file}")
        self.save_dict_to_csv(data_dict)
        logging.info("Done")
