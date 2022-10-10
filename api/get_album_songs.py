from typing import Any, Dict, List

from api.base import Base


class GetAlbumSongs(Base):
    def get_album_songs(self, uri: str) -> List[Dict[str, Any]]:
        results = self.spotify.album_tracks(uri)
        tracks  = results['items']
        while results['next']:
            results = self.spotify.next(results)
            tracks.extend(results['items'])

        return self.extract_tracks(tracks)
