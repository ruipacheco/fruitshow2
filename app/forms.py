# -*- coding: utf-8 -*-

from wtforms_alchemy import ModelForm, ModelFormField
from wtforms import widgets
from wtforms.form import Form
from wtforms.fields import TextField, PasswordField, BooleanField, DateTimeField
from wtforms.validators import Optional, required, length, email
from models import *


class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['display_hash']
        
    def populated_object(self):
        message = Message()
        self.populate_obj(message)
        return message


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['display_hash']

    def populated_object(self):
        comment = Comment()
        self.populate_obj(comment)
        return comment


class RoleForm(ModelForm):
    """ Create roles. """
    
    class Meta:
        model = Role
        exclude = ['display_hash']
    add_all_users = BooleanField(u'All existing users to new role')
    
    def populated_object(self):
        """ Returns a new model object populated with the form values. """
        
        role = Role()
        self.populate_obj(role)
        return role


class LoginForm(Form):
    """ Form used for login.
    
        Doesn't use the User model as basis because it works in a very different way.
    """
    
    identifier = TextField(u'Email or Username', [required(), length(max=255)])
    password = PasswordField(u'Password', [required(), length(max=255)])
    remember_me = BooleanField(u'Remember me')


class InviteForm(ModelForm):
    """ Form used to send invites. """
    class Meta:
        model = Invite
        exclude = ['display_hash']

    def populated_object(self):
        """ Returns a new model object populated with the form values. """
        
        invite = Invite()
        self.populate_obj(invite)
        return invite


class UserForm(ModelForm):
    """ Form used to manage users. """
    
    class Meta:
        model = User
        
    display_hash = TextField(validators=[Optional()], widget=widgets.HiddenInput())
    date_created = DateTimeField(validators=[Optional()])
    
    def populated_object(self):
        """ Returns a new model object populated with the form values. """
        
        user = User()
        self.populate_obj(user)
        return user


class ThreadForm(ModelForm):
    """ Form used to create new threads. """
    
    class Meta:
        model = Thread
        exclude = ['display_hash', 'last_updated']
    
    def populated_object(self):
        """ Returns a new object populated with the form values. """
        
        thread = Thread()
        self.populate_obj(thread)
        return thread

        
class PostForm(ModelForm):
    """ Form used to add Posts to a thread. """
    
    class Meta:
        model = Post
        exclude = ['display_hash']
    
    def populated_object(self):
        """ Returns a new model object populated with the form values. """
        
        post = Post()
        self.populate_obj(post)
        return post
