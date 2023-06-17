import aiohttp
import asyncio
from typing import List, Optional, Tuple
import json
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm.auto import tqdm

class DanbooruMetadataFetcher:
    def __init__(self, start_index: int, end_index: int, num_workers: int = 1, delay:float=0.017):
        self.start_index = start_index
        self.end_index = end_index
        self.num_workers = num_workers
        self.sema = asyncio.BoundedSemaphore(num_workers)
        self.delay = delay
        self.posts_url = "https://danbooru.donmai.us/posts/{index}.json"

    @retry(reraise=True, stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_metadata(self, index: int, session: aiohttp.ClientSession) -> Optional[dict]:
        """Fetch metadata for a single post."""
        url = self.posts_url.format(index=index)
        headers = {"User-Agent": "Mozilla/5.0"}

        async with self.sema, session.get(url, headers=headers) as response:
            if response.status == 200:
                await asyncio.sleep(self.delay)
                return await response.json()
            elif response.status == 429:
                # print(f"Rate limited at: {index}")
                await asyncio.sleep(1)  # start with a delay of 1 second
                raise Exception(f"Rate limit exceeded at index {index}")
            else:
                print(f"Received status code {response.status} for index {index}")
                body = await response.text()
                print(f"Response body: {body}")
            return None

    async def progress_wrapper(self, coro, pbar):
        """Helper function to update the progress bar."""
        result = await coro
        pbar.update(1)
        return result

    async def save_progress(self, results: List, output_path: Path):
        """Asynchronously save progress to a jsonl file."""
        with output_path.open('a') as f:  # open file in append mode
            for entry in results:
                if isinstance(entry, Exception):
                    f.write(f"{entry.__class__.__name__}: {str(entry)}\n")
                else:
                    json.dump(entry, f)
                    f.write('\n')

    async def fetch_all_metadata(self, output_filename: str) -> None:
        """Fetch metadata for all posts in the specified range and save progress every 5000 posts."""
        indices = (i for i in range(self.start_index, self.end_index - 1, -1)) if self.start_index > self.end_index else range(self.start_index, self.end_index + 1)
        output_path = Path(output_filename)
        async with aiohttp.ClientSession() as session:
            with tqdm(total=abs(self.start_index - self.end_index), desc="Fetching metadata") as pbar:
                tasks = []
                results = []
                for index in indices:
                    tasks.append(self.progress_wrapper(self.fetch_metadata(index, session), pbar))
                    if len(tasks) == 5000:
                        partial_results = await asyncio.gather(*tasks, return_exceptions=True)
                        results.extend(partial_results)
                        await self.save_progress(partial_results, output_path)
                        tasks = []
                if tasks:  # handle any remaining tasks
                    partial_results = await asyncio.gather(*tasks, return_exceptions=True)
                    results.extend(partial_results)
                    await self.save_progress(partial_results, output_path)

    def fetch_and_save(self, output_filename: str):
        """Fetch metadata and save it to a file."""
        asyncio.run(self.fetch_all_metadata(output_filename))


if __name__ == "__main__":
    fetcher = DanbooruMetadataFetcher(6408262, 6407262, num_workers=1)
    fetcher.fetch_and_save(f"dbr_meta_{fetcher.start_index}-{fetcher.end_index}.jsonl")
