import os

<<<<<<< HEAD
#SERVER SETTINGS#
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/FindFolks'
SQLALCHEMY_TRACK_MODIFICATIONS = False


DATABASE_URI = os.environ.get('DB_URL') or 'mysql://root@localhost/FindFolks'

=======
#SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/FindFolks'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') or 'mysql://root@localhost/FindFolks'
>>>>>>> ccccf7c386439e8d24822a8e89f203b987721cb1
