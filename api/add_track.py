from typing import Any, Dict

from api.base import Base
from api.get_playlist_tracks import GetPlaylistTracks


class AddTrack(Base):
    def add_song(self, track: str) -> Dict[str, Any]:
        message = "Track already in playlist."
        playlist = GetPlaylistTracks(self.party_id).get_playlist_tracks(cache=False)
        if all(t['uri'] != track for t in playlist):
            self.spotify.user_playlist_add_tracks(
                user   = self.spotify.current_user()['id'],
                playlist_id = self.playlist_id,
                tracks = [track],
            )
            message = 'Track added to playlist'
        return dict(
            message = message
        )
