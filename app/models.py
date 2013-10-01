# -*- coding: utf-8 -*-

from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import EmailType, PasswordType

import datetime
from datetime import datetime

import uuid
from uuid import uuid4


def custom_uuid():
    """ Generates a unique random numeric UUID. """
    
    return hash(str(uuid.uuid1())) % 1000000


class Category(db.Model):

    __tablename__ = 'Category'

    category_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    color = db.Column(db.Unicode(50), nullable=True)
    
    def __repr__(self):
        return u'<Category %r>' % (self.title)
        

class User(db.Model):

    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), nullable=False)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)
    display_hash = db.Column(db.String(255), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_login = db.Column(db.DateTime, nullable=True)
    email = db.Column(EmailType, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    icon = db.Column(db.String(255), nullable=True)
    
    def __init__(self, username=None, password=None, email=None):
        self.username=username
        self.password=password
        self.email=email
        self.display_hash = custom_uuid()
    
    def __repr__(self):
        return u'<User %r>' % (self.username)
        
    def generate_uuid(self):
        """ Helper method used to add or replace the UUID of a user. """
        
        self.display_hash = custom_uuid()
        
    def update_from_model(self, model):
        """ Receives a model object, usually from a form, and updates the current object with it's values. """
        
        self.username = model.username
        self.password = model.password
        self.email = model.email
        self.is_admin = model.is_admin
        self.is_deleted = model.is_deleted


class Thread(db.Model):

    __tablename__ = 'Thread'

    thread_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255), nullable=False)
    body = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    created_by = db.Column(db.Integer, ForeignKey(User.user_id))
    user = relationship(User, backref='threads')
    category_id = db.Column(db.Integer, ForeignKey(Category.category_id))
    category = relationship(Category, backref='threads')
    display_hash = db.Column(db.String(255), nullable=False, unique=True)
    spam = db.Column(db.Boolean, nullable=False, default=False)
    display_name = db.Column(db.Unicode(255), nullable=True)
    
    def __init__(self, title=None, body=None, category_id=None, display_name=None):
        self.title = title
        self.body = self.body = body.replace('\n', '<br />')
        self.category_id = category_id
        self.display_name=display_name
        self.display_hash = custom_uuid()
    
    def __repr__(self):
        return u'<Thread %r>' % (self.title)
        
    def url_title(self):
        """ Method used to display a formatted version of the thread title, with spaces replaced by dashes."""
        
        return self.title.replace(' ', '-')


class Post(db.Model):

    __tablename__ = 'Post'

    post_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    spam = db.Column(db.Boolean, nullable=False, default=0)
    created_by = db.Column(db.Integer, ForeignKey(User.user_id))
    user = relationship(User, backref='posts')
    thread_id = db.Column(db.Integer, ForeignKey(Thread.thread_id))
    thread = relationship(Thread, backref='posts')
    display_hash = db.Column(db.String(255), nullable=False, unique=True)
    display_name = db.Column(db.Unicode(255), nullable=True)
    
    def __init__(self, body=None, thread_id=None, created_by=None, display_name=None):
        self.body = body
        self.thread_id = thread_id
        self.created_by = created_by
        self.display_name = display_name
        self.display_hash = custom_uuid()
    
    def __repr__(self):
        return u'<Post %r>' % (self.date_created)

