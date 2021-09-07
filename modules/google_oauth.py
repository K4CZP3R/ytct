import google.oauth2.credentials
import google_auth_oauthlib.flow


class GoogleOAuth:
    @staticmethod
    def get_authorization_url() -> str:
        flow = GoogleOAuth.__get_flow()
        flow.redirect_uri = "https://ytct.k4czp3r.xyz/oauth2callback"
        #flow.redirect_uri = "https://localhost:5000/oauth2callback"

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        return authorization_url
    @staticmethod
    def __get_flow():
        return google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            ['https://www.googleapis.com/auth/youtube.force-ssl','https://www.googleapis.com/auth/youtube.readonly']
        )
    @staticmethod
    def fetch_token(flask_url, flask_request_url):
        flow = GoogleOAuth.__get_flow()
        flow.redirect_uri = flask_url
        auth_response = flask_request_url
        flow.fetch_token(authorization_response=auth_response)
        return GoogleOAuth.credentials_to_dict(flow.credentials)

    @staticmethod
    def credentials_to_dict(creds:google.oauth2.credentials.Credentials):
        return {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }

