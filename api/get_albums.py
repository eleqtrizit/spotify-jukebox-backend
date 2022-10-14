from collections import OrderedDict

from api.base import Base
from common.cache import cacher


class GetAlbums(Base):
    @cacher
    def get_albums(self, uri: str) -> OrderedDict:
        results = self.spotify.artist_albums(uri, album_type='album')
        albums  = results['items']
        while results['next']:
            results = self.spotify.next(results)
            albums.extend(results['items'])

        album_list = OrderedDict()
        for album in albums:
            key = album['name'].lower()
            if key not in album_list or album['total_tracks'] > album['total_tracks']:
                album_list[key] = dict(
                    name  = album['name'],
                    id    = album['id'],
                    uri   = album['uri'],
                    image = self._extract_image(album['images']),
                )

        return list(album_list.values())
