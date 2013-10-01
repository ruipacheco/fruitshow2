# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.markdown import Markdown

app = Flask(__name__)
Markdown(app)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

from app import views, models, forms