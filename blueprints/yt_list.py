from flask import Blueprint, render_template, session, redirect, render_template, url_for, request, copy_current_request_context
from modules.youtube_api import YouTubeApi
from modules.flask_redirect import FlaskRedirect
from routes import yt_list as r
import asyncio
from concurrent.futures import ThreadPoolExecutor
from decorators.google_logged_in import google_logged_in

yt_list = Blueprint('yt_list', __name__)

async def get_channels(s_credentials, ids_to_fetch):
    channels = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                YouTubeApi.get_channel_by_id,
                *(s_credentials, i)
            )
            for i in ids_to_fetch
        ]
        for c in await asyncio.gather(*tasks):
            if c is not None:
                channels.append(c)
            pass
    return channels


@yt_list.route(r.index.route_path, methods=r.index.http_types)
@google_logged_in
def index():
    cl = get_channel_list()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(get_channels(session['credentials'], cl))
    loop.run_until_complete(future)

    channels = future.result()

    pl = get_playlist_list()
    return render_template("yt_list_index.html", channels=channels,playlists=pl, ids=",".join(cl), pids=",".join(pl))


@yt_list.route(r.add.route_path, methods=r.add.http_types)
def add(channel_id: str):
    cl = get_channel_list()
    if channel_id not in cl and len(channel_id) == 24:
        cl.append(channel_id)
        set_channel_list(cl)
    return redirect(FlaskRedirect.get(url_for("search")))


@yt_list.route(r.add_playlist.route_path, methods=r.add_playlist.http_types)
def add_playlist(playlist_id: str):
    pl = get_playlist_list()
    if playlist_id not in pl:
        pl.append(playlist_id)
        set_playlists_list(pl)
    return redirect(FlaskRedirect.get(url_for("search")))


@yt_list.route(r.remove.route_path, methods=r.remove.http_types)
def remove(channel_id: str):
    cl = get_channel_list()
    if channel_id in cl and len(channel_id) == 24:
        cl.remove(channel_id)
        set_channel_list(cl)
    return redirect(FlaskRedirect.get(url_for("yt_list.index")))

@yt_list.route(r.remove_playlist.route_path, methods=r.remove_playlist.http_types)
def remove_playlist(playlist_id: str):
    pl = get_playlist_list()
    if playlist_id in pl:
        pl.remove(playlist_id)
        set_playlists_list(pl)
    return redirect(FlaskRedirect.get(url_for("yt_list.index")))

@yt_list.route(r.reset.route_path, methods=r.reset.http_types)
def reset():
    set_channel_list([])
    return redirect(FlaskRedirect.get(url_for("search")))


def get_channel_list() -> list:
    if "channels" not in session:
        return list()
    return session["channels"]

def get_playlist_list() -> list:
    if "playlists" not in session:
        return list()
    return session["playlists"]

def set_playlists_list(playlists: list):
    session["playlists"] = playlists

def set_channel_list(channels: list):
    session["channels"] = channels
