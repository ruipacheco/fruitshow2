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

import datetime
from datetime import datetime


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
            
            #TODO Flash message if this fails
            if user and pbkdf2_sha512.verify(form.password.data, user.password.hash) and login_user(user, remember=form.remember_me.data):
                user.login()
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
        post = db.session.query(func.max(Post.id), Post.display_hash).filter(Post.thread==thread).one()
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
                if len(form.display_name.data) == 0:
                    thread.user = current_user
                else:
                    thread.display_name = current_user.username
                    thread.user = None
            db.session.add(thread)
            db.session.commit()
            
            return redirect(url_for('thread', display_hash=thread.display_hash, title=thread.slug()))
            
    if request.method == 'GET':
        form = ThreadForm()
    
    return render_template('new_thread.html', form=form)


@app.route('/thread/<string:display_hash>/<string:title>', methods=['GET', 'POST'])
def thread(display_hash=None, title=None):
    """ Add comments to an existing thread. """
    
    if display_hash is None:
        abort(404)
    
    thread = Thread.query.filter(Thread.display_hash==display_hash).first()
    if not thread:
        abort(404)
        
    if not current_user.is_active() and thread.user is not None:
        abort(403)
    
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
    
    user = User(email=invite.email)
    user.generate_uuid()
    db.session.add(user)
    db.session.delete(invite)
    db.session.commit()
    
    return redirect(url_for('user', display_hash=user.display_hash))


# Actions that require users to be logged in

@app.route('/post/<string:display_hash>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(display_hash=None, action=None):
    """ Edit an existing post. Make sure we can only edit our own posts. """
    
    if display_hash == None:
        abort(404)
    
    post = Post.query.filter(Post.display_hash==display_hash).first()
    if not post:
        abort(404)
    
    if current_user != post.user:
        abort(403)
    
    if request.method == 'POST':
        form = PostForm(request.form)
        if form.validate():
            new_post = form.populated_object()
            post.body = new_post.body
            db.session.commit()
            return redirect(url_for('thread', display_hash=post.thread.display_hash, title=post.thread.slug()))
    
    if request.method == 'GET':
        form = PostForm(obj=post)
    
    return render_template('post.html', form=form, post=post)


@app.route('/sendmessage', methods=['GET', 'POST'])
@login_required
def send_message():
    """ Send a message to a number of users. """
    
    if request.method == 'POST':
        form = MessageForm(request.form)
        #TODO If not recipients, flash message
        if form.validate() and 'recipients' in request.form:
            message = form.populated_object()
            message.sender = current_user
            message.last_updated = datetime.now()
            for display_hash in request.form.getlist('recipients'):
                user = User.query.filter(User.display_hash==display_hash).first()
                if user:
                    user_message = UserMessage()
                    user_message.recipient = user
                    user_message.last_viewed = datetime.now()
                    message.recipients.append(user_message)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('messages'))
    
    if request.method == 'GET':
        form = MessageForm()
    
    users = User.query.filter(User.id!=current_user.id).all()
    return render_template('send_message.html', form=form, users=users)


@app.route('/messages', methods=['GET'])
@login_required
def messages():
    """ List sent and received messages. """
    
    def message_last_viewed(message=None):
        return db.session.query(func.max(UserMessage.last_viewed)).filter(UserMessage.message==message).first()[0]
    
    sent_messages = OrderedDict()
    for message in current_user.sent_messages:
        last_viewed = message_last_viewed(message)
        if message.sender_last_viewed != None and last_viewed > message.sender_last_viewed:
            sent_messages[message] = True
        else:
            sent_messages[message] = False
    
    received_messages = OrderedDict()
    for message in current_user.received_messages:
        last_viewed = message_last_viewed(message)
        if message.sender_last_viewed > last_viewed:
            date_viewed = last_viewed
        else:
            date_viewed = message.sender_last_viewed
        
        user_message = current_user.received_messages[message]
        if user_message.last_viewed < date_viewed:
            received_messages[message] = True
        else:
            received_messagesvir[message] = False
    
    return render_template('messages.html', sent_messages=sent_messages, received_messages=received_messages)


@app.route('/message/<string:display_hash>', methods=['GET', 'POST'])
@login_required
def message(display_hash=None):
    """ Display a specific message. """
    
    if not display_hash:
        abort(404)
    
    #TODO Flash error message
    message = Message.query.filter(Message.display_hash==display_hash).first()
    if not message or message not in current_user.sent_messages and current_user not in message.recipients:
        return redirect(url_for('messages'))
    
    if request.method == 'POST':
        form = CommentForm(request.form)
        if form.validate():
            comment = form.populated_object()
            comment.sender = current_user
            comment.message = message
            message.last_updated = datetime.now()
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('message', display_hash=display_hash))
        
    if request.method == 'GET':
        if current_user == message.sender:
           message.sender_last_viewed = datetime.now()
           db.session.commit()
        else:
            user_message = UserMessage.query.filter(UserMessage.message==message, UserMessage.recipient==current_user).first()
            user_message.last_viewed = datetime.now()
            db.session.commit()
        form = CommentForm()
        
    return render_template('message.html', message=message, form=form)


@app.route('/invite', methods=['GET', 'POST'])
@login_required
def invite():
    """ Send an email to a user inviting him to join the forum.
    
        The email will contain a link with a hash used to idenfity the invitation
        and control the timeout.
    """
    
    if not current_user.is_citizen() or not current_user.is_admin():
        return redirect(url_for('index'))
    
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


@app.route('/role', methods=['GET', 'POST'])
@login_required
def role(page=1):
    """ Create and list roles. """
    
    if not current_user.is_admin():
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        if 'display_hash' in request.form:
            display_hash = request.form['display_hash']
            role = Role.query.filter(Role.display_hash==display_hash).first()
            #TODO Flash message if role does not exist
            if role:
                db.session.delete(role)
                db.session.commit()
                return redirect(url_for('role', page=page))
        
        form = RoleForm(request.form)
        if form.validate():
            existing_role = Role.query.filter(Role.title==form.title.data).first()
            #TODO If role exists, flash message
            if not existing_role:
                role = form.populated_object()
                if form.add_all_users.data:
                    role.users = User.query.all()
                
                db.session.add(role)
                db.session.commit()
                return redirect(url_for('role', page=page))
        
    if request.method == 'GET':
        form = RoleForm()
    
    pagination = Role.query.paginate(page, CONVERSATIONS_PER_PAGE, False)    
    return render_template('roles.html', pagination=pagination, form=form)


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users(page=1):
    """ List all users. """
    
    if request.method == 'POST':
        if 'warning_display_hash' in request.form:
            display_hash = request.form['warning_display_hash']
            user = User.query.filter(User.display_hash==display_hash).first()
            
            if current_user.is_admin() or current_user.display_hash == user.display_hash:
                return render_template('warning.html', user=user)
            else:
                return redirect(url_for('users'))
            
        if 'display_hash' in request.form:
            display_hash = request.form['display_hash']
            user = User.query.filter(User.display_hash==display_hash).first()
            if current_user.is_admin() or current_user.display_hash == user.display_hash:
                db.session.delete(user)
                db.session.commit()
            return redirect(url_for('users'))
    
    pagination = User.query.paginate(page, CONVERSATIONS_PER_PAGE, False)
    return render_template('users.html', pagination=pagination)


@app.route('/user', methods=['GET', 'POST'])
@login_required
def add_user():
    """ CRUD for adding a user. """
    
    if not current_user.is_admin():
        return redirect('users')
    
    if request.method == 'POST':
        form = UserForm(request.form)
        
        if form.validate():
            existing_user = User.query.filter(User.username==form.username.data).first()
            if existing_user:
                #TODO Set error to be displayed (flash?)
                return redirect(url_for('users'))
                
            user = form.populated_object()
            user.generate_uuid()
            db.session.add(user)
            db.session.commit()        
            return redirect(url_for('users'))
        
    if request.method == 'GET':
        form = UserForm()
        
    action = url_for('add_user')
    roles = Role.query.all()
    return render_template('user.html', form=form, action=action, roles=roles)


@app.route('/user/<string:display_hash>', methods=['GET', 'POST'])
@login_required
def user(display_hash=None, action=None):
    """ Create or edit a user. """
    
    if not display_hash:
        abort(404)
    
    user = User.query.filter(User.display_hash==display_hash).first()
    if not user:
        abort(404)
    
    if request.method == 'POST':
        form = UserForm(request.form)
        
        if form.validate():
            #TODO Flash message if this condition is not met
            if form.display_hash.data == current_user.display_hash or current_user.is_admin():
                user = User.query.filter(User.display_hash==form.display_hash.data).first()
                user.update_from_model(user)
                
                if current_user.is_admin():
                    user.roles = []
                    for display_hash in request.form.getlist('role'):
                        role = Role.query.filter(Role.display_hash==display_hash).first()
                        user.roles.append(role)
                db.session.commit()
                return redirect(url_for('users'))
    
    if request.method == 'GET':
        form = UserForm(obj=user)
        
    action = url_for('user', display_hash=user.display_hash)
    roles = Role.query.all()
    return render_template('user.html', form=form, action=action, roles=roles, user=user)


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
    
