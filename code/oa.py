import os

from flask import session, request
from flask_oauthlib.client import OAuth

oauth = OAuth()

google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_ID'),
    consumer_secret=os.environ.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
