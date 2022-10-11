from typing import Any, Dict

from api.base import Base


class AddTrack(Base):
    def add_song(self, track: str) -> Dict[str, Any]:
        self.spotify.user_playlist_add_tracks(
            user   = self.spotify.current_user()['id'],
            playlist_id = self.playlist_id,
            tracks = [track],
        )
