import os
import csv
import logging
from typing import Dict, Union
from tqdm import tqdm
from pathfinder.bcy import BcyJsonParser
import pandas as pd
import polars as pl

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
            if data_dict:
                header = ["date_rank"] + list(next(iter(data_dict.values())).keys())
                writer = csv.DictWriter(csvfile, fieldnames=header, quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for date_rank, row in data_dict.items():
                    row["date_rank"] = date_rank
                    writer.writerow(row)

    def save_dict_to_parquet(self, data_dict: dict, parquet_file: str):
        """
        Save a dictionary to a Parquet file using Polars.
        :param data_dict: dictionary to be saved
        :param parquet_file: name of the output Parquet file
        """
        if data_dict:
            # Convert the dictionary to a pandas DataFrame first
            df_pandas = pd.DataFrame.from_dict(data_dict, orient='index').reset_index()

            # Rename the 'index' column to 'date_rank'
            df_pandas.rename(columns={'index': 'date_rank'}, inplace=True)

            # Then convert pandas DataFrame to Polars DataFrame
            df = pl.from_pandas(df_pandas)

            # Rearrange the columns to have 'date_rank' first
            df = df.select(['date_rank'] + [col for col in df.columns if col != 'date_rank'])

            # Write the DataFrame to a Parquet file
            df.write_parquet(parquet_file)
        else:
            raise ValueError("Empty dictionary passed.")

    def parse_and_save(self, use_parquet: bool = True):
        """
        Parse the JSON file(s) and save the results to a CSV file or Parquet file.
        """
        if os.path.isfile(self.directory):
            data_dict = self.transform_json(self.directory)
        else:
            data_dict = self.transform_directory_jsons()

        if use_parquet:
            parquet_file = self.output_file.replace(".csv", ".parquet")
            logging.info(f"Saving to {parquet_file}")
            self.save_dict_to_parquet(data_dict, parquet_file)
        else:
            logging.info(f"Saving to {self.output_file}")
            self.save_dict_to_csv(data_dict)
        logging.info("Done")
