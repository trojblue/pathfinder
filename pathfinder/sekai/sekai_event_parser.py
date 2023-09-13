import json
from typing import List
from tqdm.auto import tqdm

import unibox


def open_event_file(file_path: str) -> dict:
    # open asset file as a json file
    with open(file_path, "r", encoding="utf-8") as f:
        asset = json.load(f)

    return asset


def find_subdicts_by_display_name(
    data: dict, contained_display_name: str
) -> List[dict]:
    """Return a list of sub-dictionaries where "WindowDisplayName" contains the given substring."""
    subdicts = []
    for talk_data in data.get("TalkData", []):
        window_display_name = talk_data.get("WindowDisplayName", "")
        if contained_display_name in window_display_name:
            subdicts.append(talk_data)
    return subdicts


def extract_relevant_fields(matching_subdicts: List[dict]) -> List[dict]:
    """Extract only the relevant fields from the list of matching sub-dictionaries."""
    extracted_dicts = []
    for subdict in matching_subdicts:
        new_dict = {
            "TalkCharacters": subdict.get("TalkCharacters", []),
            "WindowDisplayName": subdict.get("WindowDisplayName", ""),
            "Body": subdict.get("Body", ""),
        }
        voices = subdict.get("Voices", [{}])
        # Assuming only one voice entry per sub-dictionary for this example.
        voice_entry = voices[0] if voices else {}
        new_dict["Voices_VoiceId_Character2dId"] = voice_entry.get(
            "Character2dId", None
        )
        new_dict["Voices_VoiceId"] = voice_entry.get("VoiceId", "")
        new_dict["Voices_Volume"] = voice_entry.get("Volume", None)

        extracted_dicts.append(new_dict)
    return extracted_dicts


def extract_single_asset_file(file_path: str, display_name: str) -> List[dict]:
    asset_dict = open_event_file(file_path)
    subdicts = find_subdicts_by_display_name(asset_dict, display_name)
    cleaned_subdicts = extract_relevant_fields(subdicts)
    return cleaned_subdicts


def driver():
    def _save_jsonl(data: list, file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            for item in data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')


    root_dir = r"E:\sekai\event_story"
    display_name = "ネネロボ"

    asset_files = unibox.traverses(root_dir, include_extensions=[".asset"])
    all_dicts = []
    for asset_file in tqdm(asset_files):
        dicts = extract_single_asset_file(asset_file, display_name)
        all_dicts.extend(dicts)


    _save_jsonl(all_dicts, "dict_temp.jsonl")

    zou_only_id_list = []

    for i in all_dicts:
        if i["WindowDisplayName"] == "奏":
            zou_only_id_list.append(i["Voices_VoiceId"])

    # save to jsonl
    unibox.saves(zou_only_id_list, "kanade_audio_id_list.txt")


if __name__ == "__main__":
    driver()
