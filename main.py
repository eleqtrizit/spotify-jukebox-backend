

from time import sleep

import uvicorn
from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from api.auth import callback as cb
from api.auth import get_auth_url
from api.get_album_songs import GetAlbumSongs
from api.get_albums import GetAlbums
from api.get_artist_songs import GetArtistSongs
from api.get_playlist_tracks import GetPlaylistTracks
from api.search import Search

# from fastapi.responses import HTMLResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


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


@app.get("/playlist_tracks/{party_id}")
def playlist_tracks(party_id: str):
    return GetPlaylistTracks(party_id).get_playlist_tracks()


@app.websocket('/ws')
async def websocket_endpoint2(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_text('Hello')
        await sleep(1)


@app.websocket("/ws_playlist_tracks/{party_id}")
async def websocket_endpoint(websocket: WebSocket, party_id: str):
    print(f"Connection for {party_id} ================================")
    last_playlist_tracks = None
    await websocket.accept()
    rec_text = await websocket.receive_text()
    print(rec_text)
    if rec_text == "start":
        while True:
            playlist_tracks = GetPlaylistTracks(party_id).get_playlist_tracks()
            await websocket.send_json(playlist_tracks)

            if playlist_tracks != last_playlist_tracks:
                print("Sending data")
                await websocket.send_json(playlist_tracks)
                last_playlist_tracks = playlist_tracks
            sleep(2)
    print("Disconnected.")


@app.get("/search/artist/{name}/{party_id}")
def search_artist_name(name: str, party_id: str):
    # http://0.0.0.0:8000/search/artist/Ice%20Cube/c6b9d426
    return Search(party_id).search_for_artist(name)


@app.get("/search/track/{name}/{party_id}")
def search_track_name(name: str, party_id: str):
    # http://0.0.0.0:8000/search/track/american%20idiot/c6b9d426
    return Search(party_id).search_for_track(name)


@app.get("/albums/{uri}/{party_id}")
def albums_uri(uri: str, party_id: str):
    # http://0.0.0.0:8000/albums/spotify:artist:3Mcii5XWf6E0lrY3Uky4cA/c6b9d426
    return GetAlbums(party_id).get_albums(uri)


@app.get("/album/songs/{uri}/{party_id}")
def album_songs_uri(uri: str, party_id: str):
    # http://0.0.0.0:8000/album/songs/spotify:album:0Uc3ButAVMni0Dnk5FFxN2/c6b9d426
    return GetAlbumSongs(party_id).get_album_songs(uri)


@app.get("/artist/songs/{uri}/{party_id}")
def artist_songs_uri(uri: str, party_id: str):
    # http://0.0.0.0:8000/artist/songs/spotify:artist:3Mcii5XWf6E0lrY3Uky4cA/c6b9d426
    return GetArtistSongs(party_id).get_artist_songs(uri)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
