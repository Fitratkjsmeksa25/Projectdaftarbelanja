import json
import os

FILE_DATA = "shopping_data.json"


def muat_data():
    if not os.path.exists(FILE_DATA):
        return []

    try:
        with open(FILE_DATA, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    return [
        {"name": str(item["name"]), "done": bool(item.get("done", False))}
        for item in data
        if isinstance(item, dict) and item.get("name")
    ]


def simpan_data(items):
    try:
        with open(FILE_DATA, "w", encoding="utf-8") as file:
            json.dump(items, file, indent=4, ensure_ascii=False)
        return True
    except OSError:
        return False