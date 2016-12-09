import os

DATABASE_URI = os.environ.get('DB_URL') or 'mysql://root@localhost/FindFolks'
