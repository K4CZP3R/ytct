from flask import request


class FlaskRedirect:
    @staticmethod
    def get(fallback_url):
        redr_url = request.args.get("redirectUrl")
        if redr_url is None:
            return fallback_url
        return redr_url
