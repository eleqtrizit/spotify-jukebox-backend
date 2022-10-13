
import uuid
from os.path import exists
from typing import Dict

from fastapi import Request

from api.create_playlist import CreatePlaylist
from common.sp_auth import sp_auth
from misc.seed import party_mix


def get_auth_url(request: Request) -> str:
    sp_oauth = sp_auth()
    auth_url = sp_oauth.get_authorize_url()
    return {"auth_url": auth_url}


def callback(request: Request) -> Dict[str, str]:
    code       = request.query_params.get("code")
    short_code = code[::4]
    code_file   = f"/tmp/partyatmyhouse/{short_code}.json"

    party_id = None
    if exists(code_file):
        party_id = open(code_file, 'r').read()
    else:
        party_id = create_party(code_file, code)
    return {"party_id": party_id}


# TODO Rename this here and in `callback`
def create_party(code_file, code):
    result = str(uuid.uuid4()).split("-")[0]
    with open(code_file, "w") as f:
        f.write(result)

    sp_oauth = sp_auth(result)
    sp_oauth.get_access_token(code)
    CreatePlaylist(result).create_playlist(f"Jukebox_{result}")
    party_mix(result)

    return result
