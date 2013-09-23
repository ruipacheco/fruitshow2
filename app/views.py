from app import app
from flask import render_template
from models import *

@app.route('/')
@app.route('/index')
def index():
    threads = Thread.query.filter(Thread.display_name != None).all()
    print len(threads)
    return render_template("index.hml")
