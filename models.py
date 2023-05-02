import os

from .app import db

from flask import current_app
from flask_login.mixins import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy import event

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_private_user_path(self):
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        
        path = os.path.join(UPLOAD_FOLDER, 'user{id}'.format(id=self.id), 'private', '')
        
        os.makedirs(path, exist_ok=True)
        
        return path
        
    def get_public_user_path(self):
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        
        path = os.path.join(UPLOAD_FOLDER, 'user{id}'.format(id=self.id), 'public', '')
        os.makedirs(path, exist_ok=True)
        
        return path
        
    def __repr__(self):
        return '<User %r>' % self.username

@event.listens_for(User.username, 'set', retval=True)
def toLowerUsername(target, value, oldvalue, initiator):
    if value is None:
        return None
    
    return value.lower()
