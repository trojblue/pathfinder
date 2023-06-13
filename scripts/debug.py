import requests
import polars as pl
from pathfinder.bcy import BcyWriter, BcyAPI

def try_get_page():
    url = "https://bcy.net/illust/toppost100?type=week&date=20230612"
    res = requests.get(url)

    # save response html to file
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(res.text)
    pass


def try_read_csv():
    df = pl.read_csv("../output.csv")

    df.write_parquet("test_from_csv.parquet")
    print(df.head(10))


def try_parse_csv():
    # Instantiate the BcyWriter
    file = r"D:\CSC\pathfinder\bcy_2015_2019\illust_week_20150920_1.json"
    writer = BcyWriter(file, "out.csv")

    # Parse the JSON files and save the results
    writer.parse_and_save(use_parquet=False)


def try_single_page():

    params = {
        "p": str(1),
        "ttype": "illust",
        "sub_type": "week",
        "date": str(20150920),
    }
    api = BcyAPI()
    api.fetch_data([params], target_dir="")

if __name__ == "__main__":
    try_parse_csv()
