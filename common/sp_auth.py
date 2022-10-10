from typing import Optional

from spotipy.oauth2 import SpotifyOAuth


def sp_auth(party_id: Optional[str] = None) -> SpotifyOAuth:
    params = dict(
        scope        = "user-top-read,user-library-read,playlist-modify-public,playlist-modify-private",
        redirect_uri = "http://localhost:8000/callback",
        open_browser = False,
    )
    if party_id:
        params["cache_path"] = f"/tmp/partyatmyhouse/{party_id}"

    return SpotifyOAuth(**params)