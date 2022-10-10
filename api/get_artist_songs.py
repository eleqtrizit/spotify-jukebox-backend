from typing import Any, Dict, List

from api.base import Base


class GetArtistSongs(Base):
    def get_artist_songs(self, uri: str) -> List[Dict[str, Any]]:
        results = self.spotify.artist_top_tracks(uri)
        tracks  = results['tracks']
        return self.extract_tracks(tracks)
