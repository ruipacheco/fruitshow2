# -*- coding: utf-8 -*-

from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import EmailType, PasswordType
from wtforms.validators import Optional
from config import SECURITY_PASSWORD_HASH, ADMINISTRATOR_ROLE, CITIZEN_ROLE

import datetime
from datetime import datetime

import uuid
from uuid import uuid4

import re
from unidecode import unidecode


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def custom_uuid():
    """ Generates a unique random numeric UUID. """
    
    return hash(str(uuid.uuid1())) % 1000000


roles_users = db.Table('User_Role',
                        db.Column('user_id', db.Integer(), db.ForeignKey('User.id')),
                        db.Column('role_id', db.Integer(), db.ForeignKey('Role.id')))
                        
user_messages = db.Table('User_Message',
                        db.Column('message_id', db.Integer(), db.ForeignKey('Message.id')),
                        db.Column('recipient_id', db.Integer(), db.ForeignKey('User.id')))


class Role(db.Model):
    
    __tablename__ = 'Role'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    display_hash = db.Column(db.Unicode(255), nullable=False, unique=True)
    
    def __init__(self, title=None):
        self.title = title
        self.display_hash = custom_uuid()
    
    def __repr__(self):
        return u'<Role %r>' % (self.title)


class User(db.Model):

    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), nullable=False)
    password = db.Column(PasswordType(schemes=[SECURITY_PASSWORD_HASH]), nullable=True)
    display_hash = db.Column(db.Unicode(255), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_login = db.Column(db.DateTime, nullable=True)
    email = db.Column(EmailType, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=backref('users', lazy='dynamic'))
    
    def __init__(self, username=None, password=None, email=None):
        self.username = username
        if self.password:
            self.password.hash = password
        self.email = email
        self.display_hash = custom_uuid()
    
    def __repr__(self):
        return u'<User %r>' % (self.username)
        
    def update_from_model(self, model):
        """ Receives a model object, usually from a form, and updates the current object with it's values. """
        
        self.username = model.username
        if self.password:
            self.password.hash = model.password.hash
        self.email = model.email
        
    def generate_uuid(self):
        """ Helper method used to add or replace the UUID of a user. """
        
        self.display_hash = custom_uuid()
    
    def login(self):
        self.last_login = datetime.now()
        
    def is_active(self):
        return True
        
    def is_authenticated(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return self.display_hash
        
    def __role_exists(self, a_role=None):
        """ Return true if the user has the specified role. """
        
        user = User.query.join(User.roles).filter(User.id==self.id, Role.id==a_role).all()
        if user:
            return True
        return False
        
    def is_admin(self):
        """ Checks whether the user has the role Administrator """
        
        return self.__role_exists(ADMINISTRATOR_ROLE)
    
    def is_citizen(self):
        """ Checks whether the user is considered a Citizen """
        
        return self.__role_exists(CITIZEN_ROLE)


class Message(db.Model):
    
    __tablename__ = 'Message'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, ForeignKey(User.id))
    sender = relationship(User, backref='sent_messages')
    subject = db.Column(db.Unicode(255), nullable=False)
    body = db.Column(db.UnicodeText, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    display_hash = db.Column(db.Unicode(255), nullable=False)
    recipients = relationship(User, secondary=user_messages, backref=backref('received_messages', lazy='dynamic'))

    def __init__(self):
        self.display_hash = custom_uuid()
        
    def __repr__(self):
        return u'<Message %r>' % (self.subject)


class Invite(db.Model):
    
    __tablename__ = 'Invite'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    display_hash = db.Column(db.Unicode(255), nullable=False)

    def __init__(self, email):
        self.email = email
        self.display_hash = custom_uuid()

    def __repr__(self):
        return u'<Invite %r>' % (self.display_hash)


class Thread(db.Model):

    __tablename__ = 'Thread'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255), nullable=False)
    body = db.Column(db.UnicodeText, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    created_by = db.Column(db.Integer, ForeignKey(User.id))
    user = relationship(User, backref='threads')
    display_hash = db.Column(db.Unicode(255), nullable=False, unique=True)
    display_name = db.Column(db.Unicode(255), nullable=True)
    nsfw = db.Column(db.Boolean, nullable=False, default=False)
    last_updated = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, title=None, body=None, category_id=None, display_name=None):
        self.title = title
        self.body = body
        self.category_id = category_id
        self.display_name = display_name
        self.display_hash = custom_uuid()
        self.last_updated = self.date_created
    
    def __repr__(self):
        return u'<Thread %r>' % (self.title)
        
    def slug(self):
        """ Generates an ASCII-only slug. """
        
        result = []
        for word in _punct_re.split(self.title.lower()):
            result.extend(unidecode(word).split())
        return unicode(u'-'.join(result))


class Post(db.Model):

    __tablename__ = 'Post'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.UnicodeText, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    created_by = db.Column(db.Integer, ForeignKey(User.id))
    user = relationship(User, backref='posts')
    thread_id = db.Column(db.Integer, ForeignKey(Thread.id))
    thread = relationship(Thread, backref='posts')
    display_hash = db.Column(db.Unicode(255), nullable=False, unique=True)
    display_name = db.Column(db.Unicode(255), nullable=True)
    
    def __init__(self, body=None, thread_id=None, created_by=None, display_name=None):
        self.body = body
        self.thread_id = thread_id
        self.created_by = created_by
        self.display_name = display_name
        self.display_hash = custom_uuid()
        self.date_created = datetime.now()
    
    def __repr__(self):
        return u'<Post %r>' % (self.date_created)
