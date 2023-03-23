import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = 'media/uploads/'

class Config(object):
    TESTING = False
    SECRET_KEY='megahipersecretkey'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG=True
    UPLOAD_FOLDER = UPLOAD_FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(ROOT_DIR, "database.sqlite"))
    
