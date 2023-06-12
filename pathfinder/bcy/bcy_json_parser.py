import os
import orjson
import logging

logging.basicConfig(level=logging.INFO)


class BcyJsonParser:
    CURR_ITEM_KEYS = [
        "item_id",
        "uid",
        "uname",
        "odin_uid",
        "ctime",
        "type",
        "plain",
        "detail_plain",
        "view_count",
        "like_count",
        "reply_count",
        "share_count",
        "mtime",
        "rtime",
        "favor_num",
        "value_user",
    ]
    CURR_DETAIL_KEYS = ["rank", "stime", "count", "wave"]

    def __init__(self, target_dir: str = "jsons"):
        self.target_dir = target_dir  # <- useless?

    def _load_json(self, file_path: str) -> dict:
        """Loads JSON data from a file and returns it.

        Args:
            file_path: Path to the JSON file to be read.

        Returns:
            Parsed JSON data as a dictionary.

        Raises:
            FileNotFoundError: If file does not exist or cannot be accessed.
            ValueError: If file content is not valid JSON.
        """
        try:
            with open(file_path, "rb") as f:
                return orjson.loads(f.read())
        except (FileNotFoundError, IOError) as e:
            logging.error(f"Unable to open file: {file_path}, {e}")
            raise FileNotFoundError(f"Unable to open file: {file_path}")
        except orjson.JSONDecodeError as e:
            logging.error(f"Invalid JSON in file: {file_path}, {e}")
            raise ValueError(f"Invalid JSON in file: {file_path}")

    def _get_info_list(self, json_data: dict) -> list:
        """Extracts 'top_list_item_info' from the data.

        Args:
            json_data: The JSON data from which to extract 'top_list_item_info'.

        Returns:
            The 'top_list_item_info' list.

        Raises:
            ValueError: If 'data' or 'top_list_item_info' is not present in json_data.
        """
        try:
            return json_data["data"]["top_list_item_info"]
        except KeyError as e:
            logging.error(f"Missing key in JSON data: {e}")
            raise ValueError(f"Invalid JSON structure, missing key: {e}")

    def _extract_item_info(self, info: dict) -> dict:
        """Extracts item and detail information from a single info dictionary.

        Args:
            info: The dictionary containing 'item_detail' and 'top_list_detail'.

        Returns:
            A dictionary with combined item and detail information.
        """
        curr_item = info.get("item_detail", {})
        curr_detail = info.get("top_list_detail", {})

        curr_info_dict = {key: curr_item.get(key, None) for key in self.CURR_ITEM_KEYS}
        curr_info_dict.update(
            {key: curr_detail.get(key, None) for key in self.CURR_DETAIL_KEYS}
        )

        # Special handling for nested dicts in curr_detail
        if curr_detail.get("ttype_set"):
            curr_info_dict["ttype"] = curr_detail["ttype_set"].get("type", None)
        if curr_detail.get("sub_type_set"):
            curr_info_dict["sub_type"] = curr_detail["sub_type_set"].get("type", None)

        return curr_info_dict

    def parse_json(self, file_path: str) -> dict:
        """Parses JSON data from a file and extracts specific information.

        Args:
            file_path: Path to the JSON file to be parsed.

        Returns:
            A dictionary containing parsed and extracted information.
        """
        json_data = self._load_json(file_path)
        info_list = self._get_info_list(json_data)

        parsed_dict = {}

        for info in info_list:
            curr_info_dict = self._extract_item_info(info)

            key_str = f"{curr_info_dict.get('stime', '00000000')}_{curr_info_dict.get('rank', '99')}"
            parsed_dict[key_str] = curr_info_dict

        return parsed_dict
