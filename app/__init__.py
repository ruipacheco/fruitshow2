# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.misaka import Misaka

app = Flask(__name__)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
Misaka(app)

from app import views, models, forms