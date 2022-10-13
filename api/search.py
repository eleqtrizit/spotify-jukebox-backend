from typing import Any, Dict

from api.base import Base


class Search(Base):
    def search(self, name: str) -> Dict[str, Any]:
        name = name.replace(' ', '')
        if not name:
            return dict(
                tracks   = [],
                albums   = [],
                artists  = [],
            )
        search_results = self.spotify.search(q=f'artist:{name}', type='artist,track,album', limit=10)
        return dict(
            artists = self.extract_artists(search_results['artists']['items']),
            tracks  = self.extract_tracks(search_results['tracks']['items']),
            albums  = self.extract_albums(search_results['albums']['items']),
        )
