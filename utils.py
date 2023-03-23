import os

from functools import wraps

from flask import abort
from flask_login import current_user

def get_path_folders_and_files(path):
    files = []
    folders = []
    
    for f in os.scandir(path):
        if f.is_dir():
            folders.append(f)
            
        else:
            files.append(f)
        
    
    return files, folders

def is_private_path(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        user_path = current_user.get_private_user_path().split(os.sep)
        
        if f'user{current_user.id}' != user_path[2]:
            abort(404, description='Not found!')
            
        return f(*args, **kwargs)
    
    return decorated_view
        