# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.misaka import Misaka
from flask.ext.mail import Mail
from micawber.providers import bootstrap_basic
from micawber.contrib.mcflask import add_oembed_filters

app = Flask(__name__)

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
Misaka(app)
oembed_providers = bootstrap_basic()
add_oembed_filters(app, oembed_providers)

from app import views, models, forms