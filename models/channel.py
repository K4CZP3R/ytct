
class ChannelEntries:
    name = "name"
    cid = "cid"
    description = "description"
    picture = "picture"


class Channel(object):
    def __init__(self, name, cid, description, picture):
        self.name = name
        self.cid = cid
        self.description = description
        self.picture = picture

    @classmethod
    def from_dict(cls, i: dict):
        return cls(
            name=i[ChannelEntries.name],
            cid=i[ChannelEntries.cid],
            description=i[ChannelEntries.description],
            picture=i[ChannelEntries.picture]
        )

    def to_dict(self) -> dict:
        return {
            ChannelEntries.name: self.name,
            ChannelEntries.cid: self.cid,
            ChannelEntries.description: self.description,
            ChannelEntries.picture: self.picture
        }