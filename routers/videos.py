from fastapi import APIRouter
from exceptions.ytct_missing_data import YtctMissingData
from fastapi import Header
from typing import Optional
from modules.youtube_api import YoutubeApi
router = APIRouter()


@router.get("/channel/{channel_id}")
async def channel(channel_id: str, creds: Optional[str] = Header(None)):
    if creds is None:
        raise YtctMissingData("Credentials are not provided!")

    return YoutubeApi.videos_by_channel_id(creds, channel_id)

@router.get("/playlist/{playlist_id}")
async def playlist_url(playlist_id: str, creds: Optional[str] = Header(None)):
    if creds is None:
        raise YtctMissingData("Credentials are not provided!")
    return YoutubeApi.videos_by_playlist_id(creds, playlist_id)