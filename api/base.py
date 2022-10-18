
from os.path import exists
from typing import Any, Dict, List, Union

import spotipy

from common.cache import STORAGE, load_cache, write_cache
from common.sp_auth import sp_auth


class Base:
    def __init__(self, party_id: str) -> None:
        self.party_id           = party_id
        self.playlist_file       = f"{party_id}_playlist.json"
        self.playlist_cache_file = f"{party_id}_playlist_cache.json"

        if not self.error_if_invalid():
            sp_oauth = sp_auth(party_id)
            token    = sp_oauth.get_access_token()
            spotipy.Spotify(auth=token["access_token"])

    def error_if_invalid(self) -> Union[None, Dict[str, any]]:
        return None if exists(f"{STORAGE}/{self.playlist_file}") else {"valid": False}

    @property
    def playlist_tracks(self):
        tracks = load_cache(self.playlist_cache_file)
        if not tracks:
            write_cache(
                fiile = self.playlist_cache_file,
                data  = self._get_playlist_tracks()
            )
        return tracks

    @property
    def playlist_tracks_no_cache(self):
        tracks = self._get_playlist_tracks()
        write_cache(self.playlist_cache_file, tracks)
        return tracks

    def _get_playlist_tracks(self):
        results = self.spotify.user_playlist_tracks(
            user        = self.spotify.current_user()['id'],
            playlist_id = self.playlist_id,
            limit       = 100
        )
        tracks  = results['items']
        while results['next']:
            results = self.spotify.next(results)
            tracks.extend(results['items'])
        # unwrap tracks
        return self.extract_tracks([track['track'] for track in tracks])

    @property
    def playlist_info(self) -> Union[Dict[str, Any], None]:
        return load_cache(self.playlist_file)

    @property
    def playlist_id(self) -> Union[str, None]:
        return self.playlist_info['id'] if self.playlist_info else None

    @property
    def spotify(self):
        sp_oauth = sp_auth(self.party_id)
        token    = sp_oauth.get_access_token()
        return spotipy.Spotify(auth=token["access_token"])

    def _extract_image(self, images: List[Dict[str, Any]]) -> Union[str, None]:
        return images[0].get('url') if images else None

    def _extract_track_artists(self, track: Dict[str, Any]) -> List[Dict[str, str]]:
        track_artists = track.get('artists', [])
        return [
            dict(
                name = artist['name'],
                uri  = artist['uri'],
                id   = artist['id'],
            ) for artist in track_artists]

    def extract_tracks(self, tracks) -> List[Dict[str, Any]]:
        return [
            dict(
                name    = track['name'],
                id      = track['id'],
                uri     = track['uri'],
                artists = self._extract_track_artists(track),
                album   = self.extract_album(track.get('album')),
            ) for track in tracks
        ]

    def extract_albums(self, album: List[Union[Dict[str, Any], None]]) -> Union[Dict[str, str], None]:
        return [self.extract_album(a) for a in album]

    def extract_album(self, album: Union[Dict[str, Any], None]) -> Union[Dict[str, str], None]:
        if album:
            return dict(
                name  = album['name'],
                id    = album['id'],
                uri   = album['uri'],
                image = self._extract_image(album['images']),
            )
        return None

    def extract_artists(self, artists: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        return [dict(
            name   = artist['name'],
            uri    = artist['uri'],
            id     = artist['id'],
            genres = artist['genres'],
            image  = self._extract_image(artist['images']),
        ) for artist in artists]
