from models.route import Route

prefix = "/yt_list"

index = Route.get(prefix)
add = Route.get(f"{prefix}/add/<string:channel_id>")
remove = Route.get(f"{prefix}/remove/<string:channel_id>")
reset = Route.get(f"{prefix}/reset")


def custom_add(channel_id):
    return str(add.route_path).replace("<string:channel_id>", channel_id)


def custom_remove(channel_id):
    return str(remove.route_path).replace("<string:channel_id>", channel_id)
