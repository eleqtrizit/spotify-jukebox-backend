import json
from os.path import exists
from typing import Any, Dict, Union

STORAGE = "/tmp/partyatmyhouse"


def get_filename(file: str) -> str:
    return f"{STORAGE}/{file}"


def load_cache(file: str) -> Union[Dict[str, Any], None]:
    filename = get_filename(file)
    if exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return None


def write_cache(file: str, data: Dict[str, Any]) -> None:
    filename = get_filename(file)
    with open(filename, "w") as f:
        json.dump(data, f)
