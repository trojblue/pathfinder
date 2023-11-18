import json
from typing import List, Union
from tqdm.auto import tqdm
import fire
import unibox


def open_event_file(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        asset = json.load(f)
    return asset


def find_subdicts_by_display_name(data: dict, contained_display_name: str) -> List[dict]:
    subdicts = []
    for talk_data in data.get("TalkData", []):
        window_display_name = talk_data.get("WindowDisplayName", "")
        if contained_display_name in window_display_name:
            subdicts.append(talk_data)
    return subdicts


def find_subdicts_by_body(data: dict, body_contains: str) -> List[dict]:
    subdicts = []
    for talk_data in data.get("TalkData", []):
        body = talk_data.get("Body", "")
        if body_contains in body:
            subdicts.append(talk_data)
    return subdicts


def extract_relevant_fields(matching_subdicts: List[dict]) -> List[dict]:
    extracted_dicts = []
    for subdict in matching_subdicts:
        new_dict = {
            "TalkCharacters": subdict.get("TalkCharacters", []),
            "WindowDisplayName": subdict.get("WindowDisplayName", ""),
            "Body": subdict.get("Body", ""),
        }
        voices = subdict.get("Voices", [{}])
        voice_entry = voices[0] if voices else {}
        new_dict["Voices_VoiceId_Character2dId"] = voice_entry.get("Character2dId", None)
        new_dict["Voices_VoiceId"] = voice_entry.get("VoiceId", "")
        new_dict["Voices_Volume"] = voice_entry.get("Volume", None)
        extracted_dicts.append(new_dict)
    return extracted_dicts


def extract_single_asset_file(
        file_path: str, display_name: Union[str, None] = None, body_contains: Union[str, None] = None
) -> List[dict]:
    if display_name is None and body_contains is None:
        raise ValueError("Either 'display_name' or 'body_contains' must be provided.")

    asset_dict = open_event_file(file_path)

    matching_subdicts = []
    if display_name and body_contains:
        subdicts_by_display_name = find_subdicts_by_display_name(asset_dict, display_name)
        subdicts_by_body = find_subdicts_by_body(asset_dict, body_contains)
        matching_subdicts = [d for d in subdicts_by_display_name if d in subdicts_by_body]
    elif display_name:
        matching_subdicts = find_subdicts_by_display_name(asset_dict, display_name)
    elif body_contains:
        matching_subdicts = find_subdicts_by_body(asset_dict, body_contains)

    cleaned_subdicts = extract_relevant_fields(matching_subdicts)
    return cleaned_subdicts


def _save_jsonl(data: list, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')


def driver(root_dir: str, display_name: str = None, body_contains: str = None):
    """
    Extracts relevant fields from all asset files in a directory.

    :param root_dir: The root directory to traverse.
    :param display_name: The display name to search for.q
    :param body_contains: The body text to search for.
    """
    if display_name is None and body_contains is None:
        raise ValueError("Either 'display_name' or 'body_contains' must be provided.")

    asset_files = unibox.traverses(root_dir, include_extensions=[".asset"])

    found_dicts = []
    for asset_file in tqdm(asset_files):
        dicts = extract_single_asset_file(asset_file, display_name, body_contains)
        found_dicts.extend(dicts)

    body_str = body_contains if body_contains else "all"

    chara_only_id_list = []
    for i in found_dicts:
        chara_only_id_list.append(i["Voices_VoiceId"])

    chara_only_id_list = list(set(chara_only_id_list))
    _save_jsonl(found_dicts, f"{display_name}_{body_str}_dict_temp.jsonl")
    unibox.saves(chara_only_id_list, f"{display_name}_{body_str}_audio_id_list.txt")


if __name__ == "__main__":
    # fire.Fire(driver)
    root_dir = r"E:\sekai\event_story"
    display_name = "奏"
    body_contains = "…"
    driver(root_dir, display_name, body_contains)
