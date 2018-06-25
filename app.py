from flask import Flask, redirect, url_for, session, render_template
from flask_oauth import OAuth
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from urllib.error import URLError
from urllib.request import Request, urlopen
import json


GOOGLE_CLIENT_ID = '{GOOGLE_CLIENT_ID}'
GOOGLE_CLIENT_SECRET = '{GOOGLE_CLIENT_SECRET}'
REDIRECT_URI = '/oauth2callback'

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
Bootstrap(app)

tickets = [
    {'title': 'Pipeline', 'description': 'An issue with the pipeline such as ftrack, 3D applications, Battery, Volt.', 'icon': 'fas fa-battery-full'},
    {'title': 'Systems', 'description': 'An issue with your computer, hardware, network.', 'icon': 'fas fa-desktop'},
    {'title': 'Flame', 'description': 'An issue with flame/flameassist/flare', 'icon': 'fas fa-fire'},
    {'title': 'Farm', 'description': 'An issue with the renderfarm', 'icon': 'fas fa-th'},
    {'title': 'License', 'description': 'An issue with/request for software licenses', 'icon': 'fas fa-file-contract'},
    {'title': 'Restore', 'description': 'Restore a whole/parts of a previous jobs', 'icon': 'fas fa-folder-open'},
    {'title': 'Other', 'description': '', 'icon': 'fas fa-question'}
]

oauth = OAuth()
google = oauth.remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'
    },
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET)


@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)
 

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@app.route('/')
def index():
    # google authenticate code
    # ------------------------------------------------------
    # access_token = session.get('access_token')
    # if access_token is None:
    #     return redirect(url_for('login'))
 
    # access_token = access_token[0]
    # headers = {'Authorization': 'OAuth ' + access_token}
    # userinfo_request = Request(
    #     'https://www.googleapis.com/oauth2/v1/userinfo',
    #     None,
    #     headers
    # )
    # try:
    #     userinfo_result = urlopen(userinfo_request)
    # except URLError as e:
    #     if e.code == 401:
    #         # Unauthorized - bad token
    #         session.pop('access_token', None)
    #         return redirect(url_for('login'))
    # ------------------------------------------------------

    return render_template('index.html', tickets=tickets)


class NewTicketForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    workstation = StringField('workstation', validators=[DataRequired()])


@app.route('/new_ticket', methods=('GET', 'POST'))
def new_ticket():
    form = NewTicketForm()
    if form.validate_on_submit():

        # get data from form
        # create gitlab issue from data
        # pass gitlab issue to ticket created template

        return redirect(url_for('ticket_created'))
    return render_template('new_ticket.html', form=form)


@app.route('/ticket_created/<gitlab_issue>', methods=('GET', 'POST'))
def ticket_created(gitlab_issue):
    return render_template('ticket_created.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
