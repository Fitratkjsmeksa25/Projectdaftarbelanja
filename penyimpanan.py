import json
import os

FILE_DATA = "shopping_data.json"


def ke_angka(nilai, default, minimum):
    try:
        angka = int(nilai)
    except (TypeError, ValueError):
        return default

    if angka < minimum:
        return default

    return angka


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

    hasil = []

    for item in data:

        if not isinstance(item, dict) or not item.get("name"):
            continue

        hasil.append({
            "name": str(item["name"]),
            "qty": ke_angka(item.get("qty", 1), 1, 1),
            "price": ke_angka(item.get("price", 0), 0, 0),
            "done": bool(item.get("done", False))
        })

    return hasil


def simpan_data(items):
    try:
        with open(FILE_DATA, "w", encoding="utf-8") as file:
            json.dump(items, file, indent=4, ensure_ascii=False)
        return True
    except OSError:
        return False