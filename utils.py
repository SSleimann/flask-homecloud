import os
import re

import typing as t
from functools import wraps

from flask import abort, url_for, redirect, current_app
from flask_login import current_user

from cryptography.fernet import Fernet, InvalidToken

from .models import User

class EncriptedEntry(object):
    def __init__(self, entry: os.DirEntry) -> None:
        self._entry = entry
        self._path = self._get_path_encrypted().decode('utf-8')
        self._relpath = self._get_relpath_encrypted().decode('utf-8')
    
    @property
    def path(self) -> str:
        return self._path
    
    @property
    def relpath(self) -> str:
        return self._relpath
    
    @property
    def entry(self) -> os.DirEntry:
        return self._entry
    
    def _get_path_encrypted(self) -> bytes:
        entry = self.entry
        path_encrypted= self._encrypt_path(entry.path)
        
        return path_encrypted
    
    def _get_relpath_encrypted(self) -> bytes:
        entry = self.entry
        path = entry.path
        
        _, relpath = re.split('private/|public/', string=path, maxsplit=1)
        
        relpath_encrypted = self._encrypt_path(relpath)
        
        return relpath_encrypted
    
    def _encrypt_path(self, path: str) -> bytes:
        path = path.encode('utf-8') 
        return encrypt_path(path)

def get_path_folders_and_files(path: str) -> t.Tuple[t.List[os.DirEntry], t.List[os.DirEntry]]:
    files = []
    folders = []
    
    for f in os.scandir(path):
        enc_dir = EncriptedEntry(f)
        
        if f.is_dir():
            folders.append(enc_dir)
            
        else:
            files.append(enc_dir)
            
    return files, folders

def get_user_path(user: User, 
                       access: t.Literal['private', 'public'],
                       path: str) -> str:
    if access == 'private':
        path = os.path.join(user.get_private_user_path(), path)
    else:
        path = os.path.join(user.get_public_user_path(), path)
    
    return path
    
def is_own(user: User) -> None:
    if user != current_user:
        abort(404, description='Not found!')
    
def not_logged_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('main_bp.cloud_private'))
        
        return f(*args, **kwargs)
    
    return decorated_view

def encrypt_path(path: bytes) -> bytes:
    key = current_app.config['PATH_KEY']
    f = Fernet(key)
    
    return f.encrypt(path)
    
def decrypt_path(token: bytes) -> bytes:
    key = current_app.config['PATH_KEY']
    
    f = Fernet(key)
    
    return f.decrypt(token)

def protected_path(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if kwargs['path'] == '':
            kwargs['path'] = encrypt_path(kwargs['path'].encode('utf-8')).decode('utf-8')
        
        kwargs['encpath'] = kwargs.get('path', None)
        
        try:
            decrypted_path = decrypt_path(kwargs['path'].encode('utf-8'))
        except InvalidToken:
            abort(404, description='No se encontro la ruta')
        
        kwargs['path'] = decrypted_path.decode('utf-8')
        
        return f(*args, **kwargs)
    
    return decorated_view

