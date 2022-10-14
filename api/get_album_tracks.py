from typing import Any, Dict, List

from api.base import Base
from common.cache import cacher


class GetAlbumTracks(Base):
    @cacher
    def get_album_tracks(self, uri: str) -> List[Dict[str, Any]]:
        results = self.spotify.album_tracks(uri)
        tracks  = results['items']
        while results['next']:
            results = self.spotify.next(results)
            tracks.extend(results['items'])

        return self.extract_tracks(tracks)
