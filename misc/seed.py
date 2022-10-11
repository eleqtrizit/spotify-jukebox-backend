from api.add_track import AddTrack

PARTY_MIX = [
    "spotify:track:6rrUcrhWlW3CqGYT0zxYlz",
    "spotify:track:2I1W3hcSsPIsEJfD69pHrW",
    "spotify:track:4agp6oHofabdUedr0B1krj",
    "spotify:track:0gljI0CtjpdZK6ecidfxto",
    "spotify:track:6qUEOWqOzu1rLPUPQ1ECpx",
    "spotify:track:2tY1gxCKslfXLFpFofYmJQ",
    "spotify:track:4NTSDu34al733aIuUWVJHo",
    "spotify:track:5uuJruktM9fMdN9Va0DUMl"
]


def party_mix(party_id: str) -> None:
    for track in PARTY_MIX:
        AddTrack(party_id).add_song(track)
