from typing import Any, Dict, List

from api.base import Base
from common.cache import cacher


class GetArtistTracks(Base):
    @cacher
    def get_artist_tracks(self, uri: str) -> List[Dict[str, Any]]:
        results = self.spotify.artist_top_tracks(uri)
        return self.extract_tracks(results['tracks'])
