from typing import List

from api.base import Base


class GetPlaylistTracks(Base):
    def get_playlist_tracks(self, cache: bool = True) -> List[str]:
        return self.playlist_tracks if cache else self.playlist_tracks_no_cache
