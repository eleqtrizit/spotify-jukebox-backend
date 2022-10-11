from typing import Any, Dict

from api.base import Base
from common.cache import write_cache


class CreatePlaylist(Base):
    def create_playlist(self, name: str) -> Dict[str, Any]:
        playlist = self.spotify.user_playlist_create(
            user          = self.spotify.current_user()['id'],
            name          = name,
            public        = False,
            collaborative = False,
            description   = "Jukebox"
        )

        write_cache(self.playlist_file, playlist)
