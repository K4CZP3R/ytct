from models.route import Route

prefix = "/timeline"

index = Route.get(f"{prefix}/<string:ids>")
new_index = Route.get(f"{prefix}")


def custom_index(ids):
    return str(index.route_path).replace("<string:ids>", ids)
