# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.misaka import Misaka
from micawber.providers import bootstrap_basic
from micawber.contrib.mcflask import add_oembed_filters

app = Flask(__name__)

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
Misaka(app)

oembed_providers = bootstrap_basic()
add_oembed_filters(app, oembed_providers)

from app import views, models, forms