from app import app
from flask import render_template, redirect
from models import *

@app.route('/')
@app.route('/index')
def index():
    threads = 

@app.route('/login')
def login():
    
    if 'email' not in request.form or 'password' not in request.form:
        return redirect('/', 302)
    
    #hash the password
    hashed_password = ''
    
    user = User.query.filter_by(email=request.form['email'], password=hashed_password).first()
    if user is None:
        # flash message
        return redirect('/', 302)
    
    return redirect('/discussions', 302)

@app.route('/discussions')
def discussions():
    pass