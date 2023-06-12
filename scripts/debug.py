import requests
import polars as pl


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


if __name__ == "__main__":
    try_read_csv()
