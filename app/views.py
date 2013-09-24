# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, redirect, url_for
from models import *
from forms import *


@app.route('/')
@app.route('/index')
def index():
    """ Lists all threads. """
    
    threads = Thread.query.filter(Thread.display_name!=None).all()
    return render_template('index.html', threads=threads)


@app.route('/thread', methods=['GET', 'POST'])
def new_thread():
    """ Displays the UI to create a new thread. """
    
    form = None
    if request.method == 'POST':
        form = ThreadForm(request.form)
        
        if form.validate():
            thread = form.populated_object()
            thread.category_id = request.form['category_id']
            db.session.add(thread)
            db.session.commit()
            
            return redirect('/thread/' + thread.display_hash + '/' + thread.url_title())
            
    if request.method == 'GET':
        form = ThreadForm()
    
    categories = Category.query.filter(Category.category_id == 1).all()
    return render_template('new_thread.html', categories=categories, form=form)


@app.route('/thread/<string:display_hash>/<string:title>')
def thread(display_hash=None, title=None):
    """ Displays a thread with a text area to add a post to the thread. """
    
    if display_hash is None:
        return render_template('404.html')
    
    thread = Thread.query.filter(Thread.display_hash==display_hash).first()
    return render_template('thread.html', thread=thread)


@app.route('/post', methods=['POST'])
def new_post():
    """ Creates a new post associated with a certain thread id. """
    
    post_body = request.form['post_body']
    display_hash = request.form['display_hash']
    display_name = request.form['display_name']
    
    thread = Thread.query.filter(Thread.display_hash==display_hash).first()    
    post = Post(body=post_body, thread_id=thread.thread_id, created_by=None, display_name=display_name)    
    db.session.add(post)
    db.session.commit()
    
    return redirect('/thread/' + thread.display_hash + '/' + thread.url_title()) 

