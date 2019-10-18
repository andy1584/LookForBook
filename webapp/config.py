import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = b'ekj74836&*^@' #random bytestring
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Celery  # # # # # # # # # # # # # # # # # # # # # # # 
                                                      #
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'    #
CELERY_BROKER_URL = 'redis://localhost:6379/0'        #
                                                      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
