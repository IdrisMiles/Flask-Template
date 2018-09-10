from flask import Flask, redirect, url_for, session, render_template, request, jsonify
from flask_oauthlib.client import OAuth
from flask_bootstrap import Bootstrap
from urllib.error import URLError
from urllib.request import Request, urlopen

import os
import json


def get_google_credentials():
    '''Method to get google credentials dictionary from docker secret
    '''
    credentials_path = os.path.join('/run', 'secrets', 'google_credentials')
    if not os.path.exists:
        raise RuntimeError('Google credentials secret is not present')
    with open(credentials_path, 'r') as f:
        j = json.load(f)
        return j


app = Flask(__name__)
app.secret_key = 'development key'
app.debug = True

app.config['GOOGLE_ID'] = get_google_credentials()['web']['client_id']
app.config['GOOGLE_SECRET'] = get_google_credentials()['web']['client_secret']
REDIRECT_URI = '/oauth2callback'

Bootstrap(app)
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    request_token_params={
        'scope': 'email profile',
        'access_type': 'offline',
        'prompt': 'consent',
        'refresh_token_url': 'https://www.googleapis.com/oauth2/v4/token',
    },
    access_token_method='POST',
    access_token_url='https://www.googleapis.com/oauth2/v4/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_access_token', None)
    session.pop('google_refresh_token', None)
    return redirect(url_for('index'))


@app.route('/oauth2callback')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_access_token'] = (resp['access_token'], '')
    session['google_refresh_token'] = (resp['refresh_token'], '')
    return redirect(url_for('index'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_access_token')
    # return session.get('google_refresh_token')


@app.context_processor
def add_google_profile_to_context():
    if get_google_oauth_token():
        userinfo = google.get('userinfo')
        return {'profile': userinfo.data}
    else:
        return {'profile': None}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
