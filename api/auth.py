
import uuid

from fastapi import Request
from fastapi.responses import RedirectResponse

from common.sp_auth import sp_auth


def auth(request: Request) -> str:
    sp_oauth = sp_auth()
    auth_url = sp_oauth.get_authorize_url()
    return "<a href='" + auth_url + "'>Login to Spotify</a>"


def callback(request: Request) -> RedirectResponse:
    party_id = str(uuid.uuid4()).split("-")[0]
    code     = request.query_params.get("code")
    sp_oauth = sp_auth(party_id)
    sp_oauth.get_access_token(code)
    res = RedirectResponse(f"/authorized/{party_id}")
    res.set_cookie("id", party_id)
    return res
