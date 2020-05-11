from models.route import Route

prefix = "/yt_list"

index = Route.get(prefix)
add = Route.get(f"{prefix}/add/<string:channel_id>")
add_playlist = Route.get(f"{prefix}/add_playlist/<string:playlist_id>")
remove = Route.get(f"{prefix}/remove/<string:channel_id>")
remove_playlist = Route.get (f"{prefix}/remove_playlist/<string:playlist_id>")
reset = Route.get(f"{prefix}/reset")


def custom_add(channel_id):
    return str(add.route_path).replace("<string:channel_id>", channel_id)
def custom_add_playlist(playlist_id):
    return str(add_playlist.route_path).replace("<string:playlist_id>", playlist_id)

def custom_remove(channel_id):
    return str(remove.route_path).replace("<string:channel_id>", channel_id)
def custom_remove_playlist(playlist_id):
    return str(remove_playlist.route_path).replace("<string:playlist_id>", playlist_id)