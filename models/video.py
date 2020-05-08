class VideoEntries:
    title = "title"
    thumbnail = "thumbnail"
    channel_name = "channel_name"
    url = "url"
    date = "date"


class Video(object):
    def __init__(self, title, thumbnail, channel_name, url, date):
        self.title = title
        self.thumbnail = thumbnail
        self.channel_name = channel_name
        self.url = url
        self.date = date

    @classmethod
    def from_dict(cls, i: dict):
        return cls(
            title=i[VideoEntries.title],
            thumbnail=i[VideoEntries.thumbnail],
            channel_name=i[VideoEntries.channel_name],
            url=i[VideoEntries.url],
            date=i[VideoEntries.date]
        )

    def to_dict(self) -> dict:
        return {
            VideoEntries.title: self.title,
            VideoEntries.thumbnail: self.thumbnail,
            VideoEntries.channel_name: self.channel_name,
            VideoEntries.url: self.url,
            VideoEntries.date: self.date
        }