import os
import random

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .db.guid import GUID
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    UserMixin,
    current_user
)
from oauthlib.oauth2 import WebApplicationClient

# GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
# GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

BASIC_LOWER = 1
BASIC_UPPER = 144

HARD_LOWER = 100
HARD_UPPER = 300

from config import *

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_IP}/{DB_NAME}'
# app.config['TESTING'] = True
db = SQLAlchemy(app)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


EMAIL_LENGTH = 324
PROBLEM_STRING_LENGTH = 1024
TEMPLATE_TITLE_LENGTH = 324
DIFFICULTY_NAME_LENGTH = 64

class person(UserMixin, db.Model):
    __tablename__ = 'person'
    email = db.Column(db.String(EMAIL_LENGTH), primary_key = True)  # email is id
    hard_problems_solved = db.Column(db.Integer, default=0)
    easy_problems_solved = db.Column(db.Integer, default=0)
    next_hard_problem = db.Column(db.Integer, default=random.randint(HARD_LOWER, HARD_UPPER))
    next_easy_problem = db.Column(db.Integer, default=random.randint(BASIC_LOWER, BASIC_UPPER))
    difficulty_left_off_on = db.Column(db.String(DIFFICULTY_NAME_LENGTH), default="basic")

    def __init__(self, email, hard_problems_solved=0, easy_problems_solved=0):
        self.email = email
        self.hard_problems_solved = hard_problems_solved
        self.easy_problems_solved = easy_problems_solved

    def get_id(self):
        return self.email

from .db import DBProxy

from .routes.login import *
from .routes.home import *
from .routes.service import *