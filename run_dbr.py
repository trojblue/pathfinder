import fire
from pathfinder.danbooru import DanbooruMetadataFetcher

def main(start:int, end:int, num_workers=1):
    """
    爬取danbooru的图片元数据
    :param start: The first post ID to fetch.
    :param end: The last post ID to fetch.
    :param num_workers: The number of concurrent workers to use.
    """
    start, end, num_workers = int(start), int(end), int(num_workers)
    fetcher = DanbooruMetadataFetcher(start, end, num_workers=num_workers)
    fetcher.fetch_and_save(f"dbr_meta_{fetcher.start_index}-{fetcher.end_index}.jsonl")

if __name__ == "__main__":
    fire.Fire(main)
