import os
import json
import time
import random
import logging
from typing import Dict, Any, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, wait_exponential, stop_after_attempt, before_log, after_log
import requests
from multiprocessing import cpu_count


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class BcyAPI:
    # threads = cpu_count() * 3
    threads = 1

    def __init__(
        self,
        base_url="https://bcy.net",
        endpoint="/apiv3/rank/list/itemInfo",
        short_break=(1, 0.1),
        long_break=(5, 0.5),
        fraction_break=(0.1, 0.01),
    ):
        """Initialization method."""
        self.base_url = base_url
        self.endpoint = endpoint
        self.session = requests.Session()
        self.executor = ThreadPoolExecutor(max_workers=self.threads)
        self.short_break = short_break
        self.long_break = long_break
        self.fraction_break = fraction_break
        self.logger = logger

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(3),
        before=before_log(logger, logging.DEBUG),
        after=after_log(logger, logging.DEBUG),
    )
    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Method to make requests to the server."""
        try:
            with self.session.get(
                self.base_url + self.endpoint, params=params
            ) as response:
                response.raise_for_status()
                self._take_short_break()
                return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed with {e}")
            raise

    def _save_response(
        self, response: Dict[str, Any], target_dir: str, params: Dict[str, Any]
    ) -> None:
        """Method to save response to a file."""
        filename = f"{params['ttype']}_{params['sub_type']}_{params['date']}_{params['p']}.json"
        file_path = os.path.join(target_dir, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(response, f)

    def fetch_data(self, parameters: List[Dict[str, Any]], target_dir: str) -> None:
        """Method to fetch data using parameters."""
        futures_params = {
            self.executor.submit(self._make_request, params): params
            for params in parameters
        }
        for future in as_completed(futures_params):
            params = futures_params[future]
            response = future.result()
            self._save_response(response, target_dir, params)
            self._take_long_break()
        self.executor.shutdown()

    def _take_short_break(self) -> None:
        """Method for a short break."""
        time.sleep(random.gauss(*self.short_break))

    def _take_long_break(self) -> None:
        """Method for a long break."""
        time.sleep(random.gauss(*self.long_break))

    def _take_fraction_break(self) -> None:
        """Method for a fraction break."""
        time.sleep(random.gauss(*self.fraction_break))
