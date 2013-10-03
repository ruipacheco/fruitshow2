# -*- coding: utf-8 -*-

# pagination
CONVERSATIONS_PER_PAGE = 10

# Change as necessary
SECRET_KEY = "\xefD\nj\xa7\xb3'\xc1\x9e\xef&\x13\xe7\xdf\xe0\xab\xe6\xac\x16\x84\xe60\x81v"

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@192.168.1.39/fruit_show'

MAIL_SERVER = 'smtp.google.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USE_SSL = True
MAIL_USERNAME = 'you'
MAIL_PASSWORD = 'your-password'

ADMINS = ['ruipacheco@hotmail.com']

# Set these to False on production
DEBUG = True
SQLALCHEMY_ECHO = True

# Don't change
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SESSION_PROTECTION = 'strong'
ADMINISTRATOR_ROLE = u'Administrator'
CITIZEN_ROLE = u'Citizen'
DELETED_ROLE = u'Deleted'