from models.route import Route

prefix = "/timeline"

index = Route.get(f"{prefix}/<string:ids>")


def custom_index(ids):
    return str(index.route_path).replace("<string:ids>", ids)
