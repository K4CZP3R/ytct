from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from models.yt_channel import YtChannel
from models.yt_video import YtVideo
from exceptions.ytct_missing_data import  YtctMissingData
from exceptions.google_oauth_exception import GoogleOauthException

import json


class YoutubeApi:
    @staticmethod
    def __get_yt(credentials: str):
        creds = Credentials(**json.loads(credentials))
        return build('youtube', 'v3', credentials=creds)

    @staticmethod
    def channel_by_id(credentials: str, channel_id: str):
        youtube = YoutubeApi.__get_yt(credentials)

        query = youtube.channels().list(
            part='snippet',
            id=channel_id
        )
        resp = query.execute()
        if len(resp['items']) == 0:
            raise YtctMissingData("Could not find an channel with this id!")
        return YoutubeApi.__convert_item_to_channel(resp['items'][0])


    @staticmethod
    def videos_by_channel_id(credentials: str, channel_id: str):
        channel_id = list(channel_id)
        channel_id[1] = "U"
        playlist_id = "".join(channel_id)
        return YoutubeApi.videos_by_playlist_id(credentials, playlist_id)

    @staticmethod
    def videos_by_playlist_id(credentials: str, playlist_id: str):
        youtube = YoutubeApi.__get_yt(credentials)
        query = youtube.playlistItems().list(
            part="snippet",
            maxResults=5,
            playlistId=playlist_id
        )

        try:
            executed_query = query.execute()
        except RefreshError:
            raise GoogleOauthException('Can\'t execute query')
        return YoutubeApi.__convert_items_to_video_list(executed_query['items'])

    @staticmethod
    def channel_search(credentials: str, channel_name: str):
        youtube = YoutubeApi.__get_yt(credentials)
        query = youtube.search().list(
            part="snippet",
            maxResults=5,
            q=channel_name
        )
        try:
            executed_query = query.execute()
        except RefreshError:
            raise GoogleOauthException('Can\'t execute query')
        return YoutubeApi.__convert_items_to_channel_list(executed_query['items'])

    @staticmethod
    def __convert_item_to_channel(item: dict):
        if 'channelId' not in item['snippet']:
            cid = item['id']
        else:
            cid = item['snippet']['channelId']

        return YtChannel(
            name=item['snippet']['title'],
            cid=cid,
            description=item['snippet']['description'],
            picture=item['snippet']['thumbnails']['default']['url']
        )

    @staticmethod
    def __convert_item_to_video(item: dict):
        return YtVideo(
            title=item['snippet']['title'],
            thumbnail=item['snippet']['thumbnails']['default']['url'],
            channel_name=item['snippet']['channelTitle'],
            url=f"https://youtube.com/watch?v={item['snippet']['resourceId']['videoId']}",
            date=item['snippet']['publishedAt']
        )

    @staticmethod
    def __convert_items_to_video_list(items):
        _videos = []
        for i in items:
            if i['kind'] != "youtube#playlistItem":
                continue
            _videos.append(YoutubeApi.__convert_item_to_video(i))
        return _videos

    @staticmethod
    def __convert_items_to_channel_list(items):
        _channels = []
        for i in items:
            if i['id']['kind'] != "youtube#channel":
                continue
            _channels.append(YoutubeApi.__convert_item_to_channel(i))
        return _channels
