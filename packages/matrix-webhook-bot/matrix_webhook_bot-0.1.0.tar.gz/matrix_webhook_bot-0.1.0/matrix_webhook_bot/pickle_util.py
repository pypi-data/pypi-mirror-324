import json
import os

persistent_data = "config/persistence.json"


def create_file_if_not_exists():
    if not os.path.exists(persistent_data):
        print("File does not exist, creating it.")
        with open(persistent_data, "w") as f:
            json.dump({}, f)


def save_data(k_v: dict):
    create_file_if_not_exists()

    with open(persistent_data, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    data.update(k_v)

    with open(persistent_data, "w") as f:
        json.dump(data, f, indent=4)


def get_data(key: str):
    return get_all_data().get(key, "")


def get_all_data():
    create_file_if_not_exists()
    try:
        with open(persistent_data, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}
    return data
