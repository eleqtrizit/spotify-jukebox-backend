from typing import Any, Dict

from api.base import Base


class AddTrack(Base):
    def add_song(self, playlist_id: str, track: str) -> Dict[str, Any]:
        self.spotify.user_playlist_add_tracks(
            user   = self.spotify.current_user()['id'],
            playlist_id = playlist_id,
            tracks = [track],
        )
