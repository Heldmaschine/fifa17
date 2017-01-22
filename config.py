import os
basedir = os.path.abspath(os.path.dirname(__file__))
#CSRF_ENABLED = False
SECRET_KEY = 'you-will-never-guess'
#SQLALCHEMY_DATABASE_URI = 'postgresql://testuser:yadbonusy@localhost/test1' local
MONGOALCHEMY_DATABASE = 'mzv'
MONGOALCHEMY_SERVER = 'ds055925.mlab.com'
MONGOALCHEMY_PORT = '55925'
MONGOALCHEMY_USER = 'admin'
MONGOALCHEMY_PASSWORD = 'admin'
SQLALCHEMY_DATABASE_URI = 'postgres://tdyxfojl:EsFgg37g2PhKiFzxPYd5YWrGyVTZRqvx@horton.elephantsql.com:5432/tdyxfojl'
MONGOALCHEMY_CONNECTION_STRING='mongodb://admin:admin@ds055925.mlab.com:55925/mzv'

SQLALCHEMY_TRACK_MODIFICATIONS = False
