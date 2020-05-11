from flask import url_for, request
from functools import wraps
from modules.flask_message import FlaskMessage
from modules.flask_session import FlaskSession
from flask import session


def google_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if FlaskSession.get_credentials() is None:
            session['redirect_url'] = request.url
            return FlaskMessage.get("Login required", "To continue you need to login with your Google account!", url_for("google_login"))

        return f(*args, **kwargs)
    return decorated_function
