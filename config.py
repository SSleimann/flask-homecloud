import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

class Config(object):
    TESTING = False
    SECRET_KEY='megahipersecretkey'
    CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG=True
    UPLOAD_FOLDER = 'uploads/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(ROOT_DIR, "database.sqlite"))
    
