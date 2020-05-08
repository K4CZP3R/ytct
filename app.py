from flask import Flask, redirect, url_for, request, session, jsonify, render_template
from modules.google_oauth import GoogleOAuth
from modules.youtube_api import YouTubeApi
from flask_bootstrap import Bootstrap
from blueprints.yt_list import yt_list
from blueprints.timeline import timeline
from flask_session import Session


app = Flask(__name__)
app.register_blueprint(yt_list)
app.register_blueprint(timeline)
app.secret_key = '12345678'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

bootstrap = Bootstrap(app)
youtube_api = YouTubeApi()


@app.route('/reset_session')
def reset_session():
    try:
        session.pop('credentials')
        session.pop('channels')
    except:
        pass
    return redirect(url_for('index'))


@app.route('/google_login')
def google_login():
    return redirect(GoogleOAuth.get_authorization_url())


@app.route('/')
def index():
    logged_in = 'credentials' in session
    return render_template("index.html", logged_in=logged_in)


@app.route('/search', methods=['GET', 'POST'])
def search():
    cl = session.get("channels", [])
    channel_name = request.args.get("channelName")
    channels = list()
    if channel_name is not None:
        channels = youtube_api.channel_search(session['credentials'], channel_name)
    return render_template('search.html', channels=channels, channel_name=channel_name, cl=cl)


@app.route("/oauth2callback")
def oauth2callback():
    creds_dict = GoogleOAuth.fetch_token(url_for('oauth2callback', _external=True), request.url)
    session['credentials'] = creds_dict

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
