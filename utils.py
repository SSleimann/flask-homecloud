import os

import typing as t

from flask import abort, url_for, redirect, current_app
from flask_login import current_user

from functools import wraps

from .models import User

def get_path_folders_and_files(path: str) -> t.Tuple[t.List[os.DirEntry], t.List[os.DirEntry]]:
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
    
    
def is_own(user: User) -> None:
    if user != current_user:
        abort(404, description='Not found!')
    
def not_logged_required(f):
    
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('main_bp.index'))
        
        return f(*args, **kwargs)
    
    return decorated_view

