import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = 'media/uploads/'

class Config(object):
    TESTING = False
    SECRET_KEY='megahipersecretkey'
    PATH_KEY= b'TPe1E0rNoBfTNmt5UQZqkKEngepwwREyl4sxqS8eWH0='

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG=True
    UPLOAD_FOLDER = UPLOAD_FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(ROOT_DIR, "database.sqlite"))
    
