from typing import List

from api.base import Base


class GetPlaylistTracks(Base):
    def get_playlist_tracks(self) -> List[str]:
        return self.playlist_tracks
