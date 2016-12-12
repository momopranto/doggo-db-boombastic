import os

#SERVER SETTINGS#
#DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') or 'mysql://root@localhost/FindFolks'

