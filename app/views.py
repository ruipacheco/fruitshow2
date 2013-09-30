# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, redirect, url_for
from models import *
from forms import *


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
def index():
    """ Lists all threads. """
    
    threads = Thread.query.filter(Thread.display_name!=None).all()
    return render_template('index.html', threads=threads)


@app.route('/thread', methods=['GET', 'POST'])
def new_thread():
    """ Used to create new threads for discussion. """
    
    form = None
    if request.method == 'POST':
        form = ThreadForm(request.form)
        
        if form.validate():
            thread = form.populated_object()
            thread.category_id = request.form['category_id']
            db.session.add(thread)
            db.session.commit()
            
            return redirect(url_for('thread'), display_hash=thread.display_hash, title=thread.url_title())
            
    if request.method == 'GET':
        form = ThreadForm()
    
    categories = Category.query.filter(Category.category_id == 1).all()
    return render_template('new_thread.html', categories=categories, form=form)


@app.route('/thread/<string:display_hash>/<string:title>', methods=['GET', 'POST'])
def thread(display_hash=None, title=None):
    """ Add comments to an existing thread. """
    
    def get_thread_by_hash(display_hash=None):
        return Thread.query.filter(Thread.display_hash==display_hash).first()
    
    import ipdb; ipdb.set_trace()
    form = None
    if request.method == 'POST':
        form = PostForm(request.form)
        
        if form.validate():
            thread = get_thread_by_hash(display_hash=request.form['display_hash'])
            if not thread:
                abort(404)
                
            post = form.populated_object()
            post.thread_id = thread.thread_id
            db.session.add(post)
            db.session.commit()
            
            anchor = 'p' + str(post.post_id)
            return redirect(url_for('thread', display_hash=thread.display_hash, title=thread.url_title(), _anchor=anchor))
      
    if request.method == 'GET':
        if display_hash is None:
            abort(404)
            
        form = PostForm()
        
    thread = get_thread_by_hash(display_hash=display_hash)
    if not thread:
        abort(404)
        
    return render_template('thread.html', thread=thread, form=form)


@app.route('/users')
def users():
    """ List all users. """
    
    users = User.query.filter(User.is_deleted==False).all()
    return render_template('users.html', users=users)


@app.route('/user', methods=['GET', 'POST'])
@app.route('/user/<string:display_hash>', methods=['GET'])
def user(display_hash=None, action=None):
    """ Create or edit a user. """
    
    if request.method == 'POST':
        form = UserForm(request.form)
        
        if form.validate():
            user = form.populated_object()
            
            if not form.display_hash.data:
                existing_user = User.query.filter(User.username==form.username.data).first()
                if existing_user:
                    # TODO Set error to be displayed
                    return redirect(url_for('user', display_hash=form.display_hash.data))
                    
                user.generate_uuid()
                db.session.add(user)
            else:
                registered_user = User.query.filter(User.display_hash==form.display_hash.data).first()
                registered_user.update_from_model(user)
                
            db.session.commit()
            
            return redirect(url_for('users'))
    
    if request.method == 'GET':
        if display_hash:
            user = User.query.filter(User.display_hash==display_hash).first()
            if not user:
                abort(404)
            form = UserForm(obj=user)
        else:
            form = UserForm()
            
    return render_template('user.html', form=form)
