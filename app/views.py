# -*- coding: utf-8 -*-

from app import app, login_manager
from flask import render_template, request, redirect, url_for, g, session
from flask.ext.login import current_user, login_user, logout_user, login_required
from flask.ext.mail import Message
from sqlalchemy.sql import func
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from app import mail
from models import *
from forms import *
from config import CONVERSATIONS_PER_PAGE

import collections
from collections import OrderedDict

import passlib
from passlib.hash import pbkdf2_sha512


def make_external(url):
    return urljoin(request.url_root, url)


def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    mail.send(msg)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.display_hash==userid).first()


@app.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Articles', feed_url=request.url, url=request.url_root)
    threads = Thread.query.order_by(Thread.last_updated.desc()).filter(Thread.user==None).all()
    for thread in threads:
        url = url_for('thread', display_hash=thread.display_hash, title=thread.slug())
        feed.add(thread.title, '', content_type='html', author=thread.display_name, url=url, updated=thread.last_updated, published=thread.date_created)
    return feed.get_response()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Handle user login """

    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter(User.username==form.identifier.data).first()
            if not user:
                user = User.query.filter(User.email==form.identifier.data).first()
            
            try:
                if user and pbkdf2_sha512.verify(form.password.data, user.password.hash) and login_user(user, remember=form.remember_me.data):
                    user.login()
            except Exception:
                pass
                
                return redirect(url_for('index'))
    
    if request.method == 'GET':
        form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    """ Lists all threads. """
    
    query = Thread.query.order_by(Thread.last_updated.desc())
    
    threads = OrderedDict()
    if current_user.is_active():
        pagination = query.paginate(page, CONVERSATIONS_PER_PAGE, False)
    else:
        pagination = query.filter(Thread.user==None).paginate(page, CONVERSATIONS_PER_PAGE, False)
    
    for thread in pagination.items:
        post = db.session.query(func.max(Post.id), Post.display_hash).filter(Post.thread_id==thread.id).one()
        threads[thread] = post[1]
    
    return render_template('index.html', threads=threads, pagination=pagination)


@app.route('/thread', methods=['GET', 'POST'])
def new_thread():
    """ Used to create new threads for discussion. """
    
    if request.method == 'POST':
        form = ThreadForm(request.form)
        
        if form.validate():
            thread = form.populated_object()
            if current_user.is_active():
                if form.make_public.data is True:
                    thread.display_name = current_user.username
                    thread.user = None
                else:
                    thread.display_name = None
                    thread.user = current_user
            db.session.add(thread)
            db.session.commit()
            
            return redirect(url_for('thread', display_hash=thread.display_hash, title=thread.slug()))
            
    if request.method == 'GET':
        form = ThreadForm()
    
    return render_template('new_thread.html', form=form)


@app.route('/thread/<string:display_hash>/<string:title>', methods=['GET', 'POST'])
def thread(display_hash=None, title=None):
    """ Add comments to an existing thread. """
    
    thread = Thread.query.filter(Thread.display_hash==display_hash).first()
    if not thread:
        abort(404)
        
    if not current_user.is_active() and thread.user is not None:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        form = PostForm(request.form)
        
        if form.validate():
            post = form.populated_object()
            post.thread = thread
            thread.last_updated = post.date_created
            if current_user.is_active():
                post.user = current_user
            db.session.add(post)
            db.session.commit()
            
            anchor = 'p' + str(post.display_hash)
            return redirect(url_for('thread', display_hash=thread.display_hash, title=thread.slug(), _anchor=anchor))
      
    if request.method == 'GET':
        if display_hash is None:
            abort(404)
            
        form = PostForm()
        
    return render_template('thread.html', thread=thread, form=form)


@app.route('/accept/<string:display_hash>', methods=['GET'])
def accept_invite(display_hash=None):
    """ Accept invite sent by email """
    
    if not display_hash:
        abort(404)
    
    invite = Invite.query.filter(Invite.display_hash==display_hash).first()
    if not invite:
        abort(404)
        
    user = User(username='', password='', email=invite.email)
    user.generate_uuid()
    db.session.add(user)
    db.session.delete(invite)
    db.session.commit()
    
    return redirect(url_for('user', display_hash=user.display_hash))


# Actions that require users to be logged in

@app.route('/invite', methods=['GET', 'POST'])
@login_required
def invite():
    """ Send an email to a user inviting him to join the forum 
    
        The email will contain a link with a hash used to idenfity the invitation
        and control the timeout
    """
    
    if request.method == 'POST':
        form = InviteForm(request.form)
        if form.validate():
            invite = form.populated_object()
            db.session.add(invite)
            db.session.commit()
            
            return ''
            #TODO Create email template; render template; send email
            #return redirect(url_for('invites'))
    
    if request.method == 'GET':
        form = InviteForm()
        
    return render_template('invite.html', form=form)


@app.route('/users')
@app.route('/users/<string:display_hash>', methods=['POST'])
@login_required
def users(display_hash=None, page=1):
    """ List all users. """
    
    users = User.query.all()
    return render_template('users.html', users=users, current_user=current_user)


@app.route('/user', methods=['GET', 'POST'])
@app.route('/user/<string:display_hash>', methods=['GET'])
@login_required
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
    

@app.route('/user/<string:display_hash>/conversations', methods=['GET'])
@login_required
def user_conversations(display_hash=None):
    
    if not display_hash:
        abort(404)
    
    threads = OrderedDict()
    pagination = Thread.query.order_by(Thread.id.desc()).filter(Thread.user.has(display_hash=display_hash)).paginate(page, CONVERSATIONS_PER_PAGE, False)
    for thread in pagination.items:
        post = db.session.query(func.max(Post.id)).filter(Post.thread_id==thread.id).one()
        threads[thread] = post[0]
    
    return render_template('index.html', threads=threads, pagination=pagination)
    
