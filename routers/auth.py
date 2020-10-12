from fastapi import APIRouter
from models.api_generic_response import ApiGenericResponse
from modules.google_oauth import GoogleOauth
router = APIRouter()


@router.get("/login")
async def auth():
    auth_url = GoogleOauth.get_authorization_url()
    return ApiGenericResponse(True, auth_url)

@router.get("/callback")
async def auth(code: str):
    return GoogleOauth.fetch_token(code)