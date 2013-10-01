# -*- coding: utf-8 -*-

# pagination
POSTS_PER_PAGE = 10

SECRET_KEY = "\xefD\nj\xa7\xb3'\xc1\x9e\xef&\x13\xe7\xdf\xe0\xab\xe6\xac\x16\x84\xe60\x81v"
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@192.168.1.39/fruit_show'
# Set these to False on production
DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True