#!/usr/bin/env python3

from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'google.login'
bootstrap = Bootstrap(app)

blueprint = make_google_blueprint(
    client_id="352492243073-lnjjuafjnok3gq9lj1snk4uejqcrlufg.apps.googleusercontent.com",
    client_secret="Lvaeo2cwEGcPSzr3KLTZudiu",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ],
    reprompt_consent=True,
)
app.register_blueprint(blueprint, url_prefix="/login")


from app import routes
