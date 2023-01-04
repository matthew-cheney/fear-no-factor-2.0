from math import floor

import requests
from flask_login import login_user, logout_user

from FearNoFactor import app, \
    GOOGLE_DISCOVERY_URL, client, \
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, DBProxy, person
from flask import abort
from flask import flash, send_file
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from flask import make_response
import os

# from . import Strings_List as StringList
# from .RejectLogger import RejectLogger
# from .settings import ADMIN_PATH, PM_PATH, DEFAULT_LANDING_PAGE
# from .user import User
import json
import re
import time

from functools import wraps

# from FearNoFactor.app_resources.forms import NewUserForm, NewProjectForm
import datetime

"""
2 pipelines here:

| - - - - - - - A - - - - - - - | - - - - B - - - | - - Ca - - - - Cb - - - - - - - | - - - - - D - - - - - | 
1. login (google) -> callback -> load_user ->     (newuser    | returningUser) ->    postLoadUser -> dashboard
3. testing_login ->              load_user ->     (newuser    | returningUser) ->    postLoadUser -> dashboard

A. Refer to google, cas, or bypass with testing_login to authenticate user.
Passes user email (for CAS, attach CAS_EMAIL_EXTENSION) to B

B. Receives email from A. Checks database. If user exists, sends to returningUser (with email).
If user does not exist, sends to new(cas)user with email.

Ca. Prompts for user info. Creates user in database (createnewuser). Sends to postLoadUser with email and cid.
Cb. Retireves cid from database. Sends to postLoadUser with email and cid.

D. Sets user admin. Sets email and cid cookies in user browser, returns the dashboard.

Also, User == Judge
"""


@app.route('/testinglogin/<email>/<password>', methods=["GET"])
def testing_login(email, password=''):
    if not password == 'Ry9HReDwAVNabDZ50ixucWwaQxuOZMqcYvrWvDHxARWShZ62N0asuOAnok7lGj6I':
        return 'Nice try! Go use the normal login.'
    return redirect(url_for('testing_login_redirect', email=email))

@app.route('/testingloginredirect', methods=['GET'])
def testing_login_redirect():
    email = request.args.get('email')
    return load_user(email)

@app.route("/login")
def login(base_url_override=None, mode=None):
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    base_url = base_url_override if base_url_override else request.base_url
    if base_url[-1] == '/':
        base_url = base_url[:-1]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=base_url + "/callback",
        scope=["openid", "email", "profile"],
        state=mode if mode else 'undetermined'
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    args = request.args
    mode = args.get('state', 'undetermined')
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        # unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        # picture = userinfo_response.json()["picture"]
        # users_name = userinfo_response.json()["given_name"]  # or family_name

    else:
        return "User email not available or not verified by Google.", 400

    # Begin user session by logging the user in
    return load_user(users_email, mode)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


# @login_manager.user_loader
def load_user(email, mode):
    # username = user.username
    if DBProxy.existsPerson(email):
        # User already in database
        if mode == 'basic' or mode == 'advanced':
            DBProxy.setMode(email, mode)
        return returninguser(email)
    # New user
    return newuser(email, mode)


@app.route('/newuser', methods=['GET', 'POST'])
def newuser(email, mode):
    DBProxy.createPerson(person(email=email))
    if mode == 'basic' or mode == 'advanced':
        DBProxy.setMode(email, mode)
    return postLoadUser(email)


@app.route('/login/createnewuser', methods=['POST'])
def createnewuser():
    email = request.form.get('email', None)
    if email is None:
        return redirect(url_for('home'))
    # Validate first/last names
    first_name = request.form.get('firstName')
    if ' ' in first_name:
        flash('names may not contain any spaces', 'danger')
        return newuser(email)
    last_name = request.form.get('lastName')
    if ' ' in last_name:
        flash('names may not contain any spaces', 'danger')
        return newuser(email)
    DBProxy.createPerson(person(email, request.form.get('firstName'),
                              request.form.get('lastName')))
    return postLoadUser(email)

def returninguser(email):
    return postLoadUser(email)


def postLoadUser(email):
    login_user(DBProxy.getPerson(email))
    res = make_response(redirect(url_for('home', email=email)))
    return res


@app.route("/logout_master")
def logout_master():
    logout_user()
    # encrypted_email = request.cookies.get('email', '')
    return redirect(url_for('public'))