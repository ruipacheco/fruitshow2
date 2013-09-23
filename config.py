import os
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
TEMPLATE_FOLDER = tmpl_dir

SECRET_KEY = "\xefD\nj\xa7\xb3'\xc1\x9e\xef&\x13\xe7\xdf\xe0\xab\xe6\xac\x16\x84\xe60\x81v"
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@192.168.1.39/fruit_show'