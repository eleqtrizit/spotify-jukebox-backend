import json
from typing import Any, Dict


def load_playlist(party_id: str) -> Dict[str, Any]:
    with open(f"/tmp/partyatmyhouse/{party_id}_playlist.json", "r") as f:
        playlist = f.read()
    return json.loads(playlist)


def get_playlist_id(party_id: str) -> Dict[str, Any]:
    return load_playlist(party_id)['id']
