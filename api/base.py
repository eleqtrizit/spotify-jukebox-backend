from typing import Any, Dict, List, Union

import spotipy

from common.sp_auth import sp_auth


class Base:
    def __init__(self, party_id: str) -> None:
        self.party_id = party_id
        sp_oauth      = sp_auth(party_id)
        token         = sp_oauth.get_access_token()
        spotipy.Spotify(auth=token["access_token"])

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
                album   = self._extract_album(track.get('album')),
            ) for track in tracks
        ]

    def _extract_album(self, album: Union[Dict[str, Any], None]) -> Union[Dict[str, str], None]:
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
