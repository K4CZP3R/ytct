from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from models.channel import Channel
from models.video import Video


class YouTubeApi:
    @staticmethod
    def filter_valid_ids(ids):
        valid_ids = list()
        for i in ids:
            if len(i) != 24:
                continue
            valid_ids.append(i)
        return valid_ids

    @staticmethod
    def get_videos_by_channel_id(session_credentials, channel_id):
        channel_id = list(channel_id)
        channel_id[1] = "U"
        playlist_id = "".join(channel_id)

        return YouTubeApi.get_videos_in_playlist(session_credentials, playlist_id)

    @staticmethod
    def get_videos_in_playlist(session_credentials, playlist_id):
        credentials = Credentials(**session_credentials)
        youtube = build('youtube', 'v3', credentials=credentials)
        query = youtube.playlistItems().list(
            part="snippet",
            maxResults=5,
            playlistId=playlist_id
        )

        return YouTubeApi.__convert_search_to_videos_list(query.execute())

    @staticmethod
    def channel_search(session_credentials, channel_name):
        credentials = Credentials(**session_credentials)
        youtube = build('youtube', 'v3', credentials=credentials)
        query = youtube.search().list(
            part="snippet",
            maxResults=5,
            q=channel_name
        )

        return YouTubeApi.__convert_search_to_channel_list(query.execute())

    @staticmethod
    def get_channel_by_id(session_credentials, channel_id):
        credentials = Credentials(**session_credentials)
        youtube = build('youtube', 'v3', credentials=credentials)
        query = youtube.channels().list(
            part='snippet',
            id=channel_id
        )
        resp = query.execute()
        if len(resp['items']) == 0:
            return None
        return YouTubeApi.__convert_item_to_channel(query.execute()['items'][0])

    @staticmethod
    def __convert_item_to_video(item):
        return Video(
            title=item['snippet']['title'],
            thumbnail=item['snippet']['thumbnails']['default']['url'],
            channel_name=item['snippet']['channelTitle'],
            url=f"https://youtube.com/watch?v={item['snippet']['resourceId']['videoId']}",
            date=item['snippet']['publishedAt']
        )

    @staticmethod
    def __convert_search_to_videos_list(search_result):
        videos = list()
        for i in search_result['items']:
            if i['kind'] != 'youtube#playlistItem':
                continue

            videos.append(YouTubeApi.__convert_item_to_video(i))
        return videos

    @staticmethod
    def __convert_item_to_channel(item):
        if 'channelId' not in item['snippet']:
            cid = item['id']
        else:
            cid = item['snippet']['channelId']

        return Channel(
            name=item['snippet']['title'],
            cid=cid,
            description=item['snippet']['description'],
            picture=item['snippet']['thumbnails']['default']['url']
        )

    @staticmethod
    def __convert_search_to_channel_list(search_result):
        channels = list()
        for i in search_result["items"]:
            if i['id']['kind'] != "youtube#channel":
                continue
            channels.append(YouTubeApi.__convert_item_to_channel(i))
        return channels
