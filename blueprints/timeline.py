from flask import Blueprint, render_template, session, redirect, render_template, url_for, request
from routes import timeline as r
from decorators.google_logged_in import google_logged_in
from modules.youtube_api import YouTubeApi
import asyncio
from concurrent.futures import ThreadPoolExecutor
import operator
from models.video import Video

timeline = Blueprint('timeline', __name__)


async def get_videos_of_channels_async(s_credentials, ids_to_fetch):
    videos = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                YouTubeApi.get_videos_by_channel_id,
                *(s_credentials, i)
            )
            for i in ids_to_fetch
        ]
        for u_videos in await asyncio.gather(*tasks):
            for video in u_videos:
                videos.append(video)
            pass
    return videos


@timeline.route(r.index.route_path, methods=r.index.http_types)
@google_logged_in
def index(ids):
    ids = YouTubeApi.filter_valid_ids(ids.split(','))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(get_videos_of_channels_async(session['credentials'], ids))
    loop.run_until_complete(future)

    videos = sort_videos(future.result())

    return render_template("timeline_index.html", videos=videos, timeline_url=request.url)


def sort_videos(videos):
    dict_videos = list()
    for v in videos:
        dict_videos.append(v.to_dict())
    dict_videos.sort(key=operator.itemgetter('date'))

    _videos = list()
    for v in dict_videos:
        _videos.append(Video.from_dict(v))
    _videos.reverse()
    return _videos