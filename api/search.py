from typing import Any, Dict, List

from api.base import Base


class Search(Base):
    def search_for_artist(self, name: str) -> List[Dict[str, Any]]:
        results = self.spotify.search(q=f'artist:{name}', type='artist')
        artists = results['artists']['items']
        return self.extract_artists(artists)

    def search_for_track(self, name: str) -> List[Dict[str, Any]]:
        results = self.spotify.search(q=f'track:{name}', type='track')
        tracks  = results['tracks']['items']
        return self.extract_tracks(tracks)
