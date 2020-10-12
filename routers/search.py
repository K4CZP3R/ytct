from fastapi import APIRouter
from models.api_generic_response import ApiGenericResponse
from exceptions.ytct_missing_data import YtctMissingData
from modules.youtube_api import YoutubeApi
from fastapi import Header
import json
from typing import Optional

router = APIRouter()


@router.get("/channel")
async def channel(creds: Optional[str] = Header(None), query: str = None):
    if creds is None or query is None:
        raise YtctMissingData("Credentials and/or query is not provided!")
    return YoutubeApi.channel_search(creds, query)

