import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = b'ekj74836&*^@' #random bytestring
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

#Celery
CELERY_BROKER = 'redis://localhost:6379/0'