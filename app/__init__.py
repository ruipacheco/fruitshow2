from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

from app import views, models