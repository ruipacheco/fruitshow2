# -*- coding: utf-8 -*-

from wtforms_alchemy import ModelForm, ModelFormField
from wtforms import widgets
from wtforms.form import Form
from wtforms.fields import TextField, PasswordField, BooleanField
from wtforms.validators import Optional, required, length, email
from models import *


class LoginForm(Form):
    """ Form used for login.
    
        Doesn't use the User model as basis because it works in a very different way.
    """
    
    identifier = TextField(u'Email or Username', [required(), length(max=255)])
    password = PasswordField(u'Password', [required(), length(max=255)])
    remember_me = BooleanField(u'Remember me')


class InviteForm(ModelForm):
    class Meta:
        model = Invite
        exclude = ['display_hash']

    def populated_object(self):
        """ Returns a new model object populated with the form values. """
        
        invite = Invite(self.email.data)
        self.populate_obj(invite)
        return invite


class UserForm(ModelForm):
    class Meta:
        model = User
        
    display_hash = TextField(validators=[Optional()], widget=widgets.HiddenInput())
    
    def populated_object(self):
        """ Returns a new model object populated with the form values. """
        
        user = User()
        self.populate_obj(user)
        return user


class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        exclude = ['display_hash']
    
    def populated_object(self):
        """ Returns a new object populated with the form values. """
        
        thread = Thread()
        self.populate_obj(thread)
        return thread
    
    make_public = BooleanField(u'Create public post', validators=[Optional()])

        
class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['display_hash']
    
    def populated_object(self):
        """ Returns a new model object populated with the form values. """
        
        post = Post()
        self.populate_obj(post)
        return post
