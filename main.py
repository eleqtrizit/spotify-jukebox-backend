import uvicorn
from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from api.add_track import AddTrack
from api.auth import callback as cb
from api.auth import get_auth_url
from api.base import Base
from api.get_album_tracks import GetAlbumTracks
from api.get_albums import GetAlbums
from api.get_artist_tracks import GetArtistTracks
from api.get_playlist_tracks import GetPlaylistTracks
from api.search import Search
from api.websocket_refresh_playlist import websocket_refresh_playlist

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


@app.on_event("startup")
async def startup_event():
    pass


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authorized/{party_id}")
def authorized(party_id: str):
    return {
        "authorized": True,
        "party_id": party_id,
    }


@app.get("/auth_url")
def auth_url(request: Request):
    return get_auth_url(request)


@app.get("/callback")
def callback(request: Request):
    return cb(request)


# @app.websocket('/ws')
# async def websocket_endpoint2(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         await websocket.send_text('Hello')
#         await sleep(1)


@app.websocket("/ws_playlist_tracks/{party_id}")
async def ws_playlist_tracks(websocket: WebSocket, party_id: str):
    if not error_if_invalid(party_id):
        await websocket_refresh_playlist(websocket, party_id)


@app.get("/playlist_tracks/{party_id}")
def playlist_tracks(party_id: str):
    return error_if_invalid(party_id) or GetPlaylistTracks(party_id).get_playlist_tracks(cache=False)


@app.get("/search/{query}/{party_id}")
def search(query: str, party_id: str):
    return error_if_invalid(party_id) or Search(party_id).search(query)


@app.get("/add/{track_id}/{party_id}")
def add(track_id: str, party_id: str):
    return error_if_invalid(party_id) or AddTrack(party_id).add_song(track_id)


@app.get("/albums/{uri}/{party_id}")
def albums_uri(uri: str, party_id: str):
    # http://0.0.0.0:8000/albums/spotify:artist:3Mcii5XWf6E0lrY3Uky4cA/c6b9d426
    return error_if_invalid(party_id) or GetAlbums(party_id).get_albums(uri)


@app.get("/album/tracks/{uri}/{party_id}")
def album_tracks_uri(uri: str, party_id: str):
    # http://0.0.0.0:8000/album/tracks/spotify:album:0Uc3ButAVMni0Dnk5FFxN2/c6b9d426
    return error_if_invalid(party_id) or GetAlbumTracks(party_id).get_album_tracks(uri)


@app.get("/artist/tracks/{uri}/{party_id}")
def artist_tracks_uri(uri: str, party_id: str):
    # http://0.0.0.0:8000/artist/tracks/spotify:artist:3Mcii5XWf6E0lrY3Uky4cA/c6b9d426
    return error_if_invalid(party_id) or GetArtistTracks(party_id).get_artist_tracks(uri)


@app.get("/check/{party_id}")
def check_party_id(party_id: str):
    # http://0.0.0.0:8000/check/c6b9d426
    return error_if_invalid(party_id) or {"valid": True}


def error_if_invalid(party_id):
    return Base(party_id).error_if_invalid()


if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
