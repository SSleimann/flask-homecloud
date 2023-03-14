class Config(object):
    TESTING = False
    SECRET_KEY='megahipersecretkey'

class DevelopmentConfig(Config):
    TESTING = True
    DEBUG=True
    UPLOAD_FOLDER = 'uploads/'