from flask import Flask, redirect, url_for, request, session, jsonify, render_template
from modules.google_oauth import GoogleOAuth
from modules.youtube_api import YouTubeApi
from flask_bootstrap import Bootstrap
from blueprints.yt_list import yt_list
from blueprints.timeline import timeline
from flask_session import Session
from datetime import timedelta

app = Flask(__name__)
app.register_blueprint(yt_list)
app.register_blueprint(timeline)
app.secret_key = '87654321'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
Session(app)

bootstrap = Bootstrap(app)
youtube_api = YouTubeApi()


@app.route('/session')
def sess():
    return str(session.get('credentials'))


@app.route('/reset_session')
def reset_session():
    try:
        session.pop('credentials')
        session.pop('channels')
        session.pop('playlists')
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
    playlist_url = request.args.get("playlistUrl")
    playlist_id = None
    channels = list()
    playlist_items = list()
    if channel_name is not None:
        channels = youtube_api.channel_search(session['credentials'], channel_name)
    if playlist_url is not None and "list=" in str(playlist_url):
        playlist_url: str
        start_index = playlist_url.index("list=") + len("list=")
        playlist_id = playlist_url[start_index:]
        playlist_items = youtube_api.get_videos_in_playlist(session['credentials'], playlist_id)

    return render_template('search.html', channels=channels, playlist_id=playlist_id, channel_name=channel_name, cl=cl,
                           playlist_url=playlist_url, playlist_items=playlist_items)


@app.route("/oauth2callback")
def oauth2callback():
    session.permanent = True
    creds_dict = GoogleOAuth.fetch_token(url_for('oauth2callback', _external=True), request.url)
    session['credentials'] = creds_dict

    if "redirect_url" in session:
        return redirect(session['redirect_url'])
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
