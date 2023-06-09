import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'media/uploads/')

class Config(object):
    TESTING = False
    SECRET_KEY= 'megahipersecretkey'
    PATH_KEY= b'TPe1E0rNoBfTNmt5UQZqkKEngepwwREyl4sxqS8eWH0='
    UPLOAD_FOLDER = UPLOAD_FOLDER

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(ROOT_DIR, "dev_database.sqlite"))
    
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(ROOT_DIR, "test_database.sqlite"))
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'media/uploads_testing/')