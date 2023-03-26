import os
import typing as t

from functools import wraps

from flask import abort
from flask_login import current_user

from .models import User

def get_path_folders_and_files(path):
    files = []
    folders = []
    
    for f in os.scandir(path):
        if f.is_dir():
            folders.append(f)
            
        else:
            files.append(f)
        
    
    return files, folders

def get_user_path(path: str, 
                       access: t.Literal['private', 'public']
                       ) -> t.Tuple[t.Optional[User], str]:
    
    path_splited = path.split('/') 
    access = access.lower()
    
    if access == 'private':
        user = current_user
        path = os.path.join(user.get_private_user_path(), path, '')
    
    else:
        if path.startswith('user_'):
            _, username = path_splited.pop(0).split('user_', maxsplit=1)
            user = User.query.filter_by(username=username).first()
            
        else:
            user = current_user
        
        joined_path = '/'.join(path_splited)
        
        path = os.path.join(user.get_public_user_path(), joined_path, '')
    
    return user, path
    
    
def is_own_path(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        user_path = current_user.get_private_user_path().split(os.sep)
        
        if f'user{current_user.id}' != user_path[2]:
            abort(404, description='Not found!')
            
        return f(*args, **kwargs)
    
    return decorated_view
        