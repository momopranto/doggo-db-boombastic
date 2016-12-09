import os

#SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/FindFolks'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') or 'mysql://root@localhost/FindFolks'
