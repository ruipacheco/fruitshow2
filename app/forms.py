# -*- coding: utf-8 -*-

from wtforms_alchemy import ModelForm, ModelFormField
from wtforms import widgets
from wtforms.fields import TextField
from wtforms.validators import Optional
from models import *


class CategoryForm(ModelForm):
    class Meta:
        model = Category

    def populated_object(self):
        """ Returns a new model object populated with the form values. """
        
        print '###'
        print model
        print '###'
        
        category = Category()
        self.populate_obj(category)
        return category


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

        
class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['display_hash']
    
    def populated_object(self):
        """ Returns a new model object populated with the form values. """
        
        post = Post()
        self.populate_obj(post)
        return post
