import os
import orjson


class BcyJsonParser:
    def __init__(self, target_dir: str = "jsons"):
        self.target_dir = target_dir
        os.makedirs(target_dir, exist_ok=True)

        self.json = None
        self.parsed_json = None

    def _load_json(self, file_path: str):
        """Loads JSON data from a file"""
        try:
            with open(file_path, "rb") as f:
                self.json = orjson.loads(f.read())
                return self.json
        except (FileNotFoundError, IOError) as e:
            raise FileNotFoundError(f"Unable to open file: {e}")
        except orjson.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    def parse_json(self, file_path: str) -> dict:
        """Parses and saves JSON data to a file"""
        curr_json = self._load_json(file_path)

        info_list = curr_json["data"]["top_list_item_info"]

        return_dict = {}

        # Define the keys you're interested in.
        curr_item_keys = [
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
        curr_detail_keys = ["rank", "stime", "count", "wave"]

        for info in info_list:
            curr_item = info["item_detail"]
            curr_detail = info["top_list_detail"]

            # Create a dictionary based on the keys and their values. If a key doesn't exist, None is used.
            curr_info_dict = {key: curr_item.get(key, None) for key in curr_item_keys}
            curr_info_dict.update(
                {key: curr_detail.get(key, None) for key in curr_detail_keys}
            )

            # Special handling for nested dicts in curr_detail
            if curr_detail.get("ttype_set"):
                curr_info_dict["ttype"] = curr_detail["ttype_set"].get("type", None)
            if curr_detail.get("sub_type_set"):
                curr_info_dict["sub_type"] = curr_detail["sub_type_set"].get(
                    "type", None
                )

            key_str = f"{curr_info_dict.get('stime', '00000000')}_{curr_info_dict.get('rank', '99')}"
            return_dict[key_str] = curr_info_dict

        return return_dict
