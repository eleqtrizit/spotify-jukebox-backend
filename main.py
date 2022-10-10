import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from api.auth import auth
from api.auth import callback as cb
from api.get_album_songs import GetAlbumSongs
from api.get_albums import GetAlbums
from api.get_artist_songs import GetArtistSongs
from api.search import Search

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authorized/{party_id}")
def authorized(party_id: str):
    return {
        "authorized": True,
        "party_id": party_id,
    }


@app.get("/authorize", response_class=HTMLResponse)
def authorize(request: Request):
    return auth(request)


@app.get("/callback")
def callback(request: Request):
    return cb(request)


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
