import json
from typing import Any, Dict

from api.base import Base


class CreatePlaylist(Base):
    def create_playlist(self, name: str) -> Dict[str, Any]:
        playlist = self.spotify.user_playlist_create(
            user          = self.spotify.current_user()['id'],
            name          = name,
            public        = False,
            collaborative = False,
            description   = "Jukebox"
        )
        with open(f"/tmp/partyatmyhouse/{self.party_id}_playlist.json", "w") as f:
            f.write(json.dumps(playlist))
