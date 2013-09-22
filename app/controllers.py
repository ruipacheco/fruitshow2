from app import app
from flask import render_template, redirect
from models import *

@app.route('/')
@app.route('/index')
def index():
    threads = Thread.query.filter(Thread.display_name != None).all()
    return threads
