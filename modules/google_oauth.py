import google.oauth2.credentials
import google_auth_oauthlib.flow
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
from exceptions.google_oauth_exception import GoogleOauthException
import config


class GoogleOauth:
    @staticmethod
    def get_authorization_url() -> str:
        flow = GoogleOauth.__get_flow()
        flow.redirect_uri = config.GOOGLE_REDIRECT_URI


        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        return authorization_url

    @staticmethod
    def fetch_token(google_code: str):
        flow = GoogleOauth.__get_flow()
        flow.redirect_uri = config.GOOGLE_REDIRECT_URI
        try:
            flow.fetch_token(code=google_code)
            return GoogleOauth.__credentials_to_dict(flow.credentials)
        except InvalidGrantError as e:
            raise GoogleOauthException(e.error)
        except ValueError as e:
            raise GoogleOauthException(e)

    @staticmethod
    def __get_flow():
        return google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secrets_file="credentials.json",
            scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
        )

    @staticmethod
    def __credentials_to_dict(creds: google.oauth2.credentials.Credentials):
        return {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
