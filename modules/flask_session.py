from flask import session


class FlaskSession:
    @staticmethod
    def get_credentials():
        return session.get("credentials", None)

    @staticmethod
    def set_credentials(credentials):
        session["credentials"] = credentials

    @staticmethod
    def get_channel_list():
        return session.get("channels", None)

    @staticmethod
    def set_channel_list(channels):
        session["channels"] = channels
