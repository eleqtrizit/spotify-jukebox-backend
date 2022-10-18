from time import sleep

from api.get_playlist_tracks import GetPlaylistTracks


async def websocket_refresh_playlist(websocket, party_id):
    await websocket.accept()
    print(f"Connection for {party_id} ================================")

    last_playlist_tracks = None
    text = await websocket.receive_text()
    print(text)

    counter = 0
    pl = GetPlaylistTracks(party_id)
    while True:
        playlist_tracks = pl.get_playlist_tracks(cache=False)
        await websocket.send_json(playlist_tracks)

        if playlist_tracks == last_playlist_tracks:
            await websocket.send_json({"no_change": True})
        else:
            print("Sending data")
            await websocket.send_json(playlist_tracks)
            last_playlist_tracks = playlist_tracks
        sleep(1)
        counter += 1

    print("Disconnected.")
