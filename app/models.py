from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

import datetime
from datetime import datetime


class Category(db.Model):

    __tablename__ = 'Category'

    category_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())

class User(db.Model):

    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, default='Anonymous Coward')
    password = db.Column(db.String(255), nullable=False)
    display_hash = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_login = db.Column(db.DateTime, nullable=True)
    email = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

class Thread(db.Model):

    __tablename__ = 'Thread'

    thread_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    created_by = db.Column(db.Integer, ForeignKey(User.user_id))
    user = relationship(User, backref='threads')
    category_id = db.Column(db.Integer, ForeignKey(Category.category_id))
    category = relationship(Category, backref='threads')
    display_hash = db.Column(db.String(255), nullable=False)
    spam = db.Column(db.Boolean, nullable=False, default=False)
    display_name = db.Column(db.String(255), nullable=True)

class Post(db.Model):

    __tablename__ = 'Post'

    post_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    spam = db.Column(db.Boolean, nullable=False, default=0)
    created_by = db.Column(db.Integer, ForeignKey(User.user_id))
    user = relationship(User, backref='posts')
    thread_id = db.Column(db.Integer, ForeignKey(Thread.thread_id))
    thread = relationship(Thread, backref='posts')
    display_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255), nullable=True)
