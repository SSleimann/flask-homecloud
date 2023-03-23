import os

from flask import Blueprint, render_template, redirect, url_for, current_app, request, abort
from flask_login.utils import login_required, current_user

from . import db
from .models import User
from .utils import get_path_folders_and_files, is_private_path
from .forms import CreateDirForm, FileUploadForm, SearchByUsernameForm

main_bp = Blueprint('main_bp', __name__,
                        template_folder='templates/main',
                        url_prefix='/main')


@main_bp.route('/')
@login_required
def index():
    return f'HELLOw {current_user.username}'

@main_bp.route('/cloud/private/', defaults={'path': ''}, methods=['GET', 'POST'])
@main_bp.route('/cloud/private/<path:path>')
@login_required
def cloud_private(path):
    path = os.path.join(current_user.get_private_user_path(), path, '')
    
    try:
        files, folders = get_path_folders_and_files(path)
    except FileNotFoundError:
        abort(404, description='Folder not found!')
    
    return render_template('cloud.html', files=files, folders=folders, req=request)

@main_bp.route('/cloud/public/', defaults={'path': ''}, methods=['GET', 'POST'])
@main_bp.route('/cloud/public/<path:path>')
@login_required
def cloud_public(path):
    if path.startswith('user_'):
        spath = path.split('/', maxsplit=1)
        
        _, username = spath.pop(0).split('user_', maxsplit=1)
        user = User.query.filter_by(username=username).first()
        
        path = spath[0]
    
    else:
        user = current_user
    
    path = os.path.join(user.get_public_user_path(), path, '')
    
    try:
        files, folders = get_path_folders_and_files(path)
    except FileNotFoundError:
        abort(404, description='Folder not found!')
    
    return render_template('cloud.html', files=files, folders=folders, req=request, usr=user)

