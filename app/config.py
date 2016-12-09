import os
<<<<<<< HEAD
#SERVER SETTINGS#
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/FindFolks'
SQLALCHEMY_TRACK_MODIFICATIONS = False
=======

DATABASE_URI = os.environ.get('DB_URL') or 'mysql://root@localhost/FindFolks'
>>>>>>> 75167887b52794dca9b0d5e6a076b29ab9187d8f
