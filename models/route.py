class Route(object):
    def __init__(self, route_path, http_types):
        self.route_path = route_path
        self.http_types = http_types

    @classmethod
    def get(cls, route_path):
        return cls(route_path, ['GET'])

    @classmethod
    def post(cls, route_path):
        return cls(route_path, ['POST'])

    @classmethod
    def get_post(cls, route_path):
        return cls(route_path, ['GET', 'POST'])
