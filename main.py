import os

from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login.utils import login_required, current_user

from . import db
from .utils import get_path_folders_and_files, is_own_path, get_user_path
from .forms import CreateDirForm, FileUploadForm
from .models import User

main_bp = Blueprint('main_bp', __name__,
                        template_folder='templates/main',
                        url_prefix='/main')

@main_bp.route('/cloud/private/', defaults={'path': ''}, methods=['GET', 'POST'])
@main_bp.route('/cloud/private/<path:path>', methods=['GET', 'POST'])
@login_required
def cloud_private(path):
    _, dpath = get_user_path(path, 'private')
    
    try:
        files, folders = get_path_folders_and_files(dpath)
    except FileNotFoundError:
        abort(404, description='Folder not found!')
    
    context = {
        'files': files,
        'folders': folders,
        'req': request,
        'usr': current_user,
        'form_create_dir': CreateDirForm(),
        'form_upload_file': FileUploadForm(),
        'path': os.path.join('private', path, '')
    }
    
    return render_template('cloud.html', **context)

@main_bp.route('/cloud/public/', defaults={'path': ''}, methods=['GET', 'POST'])
@main_bp.route('/cloud/public/<path:path>', methods=['GET', 'POST'])
@login_required
def cloud_public(path):
    user, dpath = get_user_path(path, 'public')
    
    try:
        files, folders = get_path_folders_and_files(dpath)
    except FileNotFoundError:
        abort(404, description='Folder not found!')
    
    context = {
        'files': files,
        'folders': folders,
        'req': request,
        'usr': user,
        'form_create_dir': CreateDirForm(),
        'form_upload_file': FileUploadForm(),
        'path': os.path.join('public', path, '')
    }
    
    return render_template('cloud.html', **context)

@main_bp.route('/cloud/create_dir/', defaults={'path': ''}, methods=['POST'])
@main_bp.route('/cloud/create_dir/<path:path>', methods=['POST'])
@login_required
def cloud_create_dir(path):
    form = CreateDirForm()
    next = request.form.get('next', None)
    
    if next is None:
        abort(400)
        
    if form.validate_on_submit():
        status, path = path.split('/', maxsplit=1)
        
        _, dpath = get_user_path(path, status.lower())
        new_dir_path = os.path.join(dpath, form.dir.data, '')
        
        try:
            os.mkdir(new_dir_path)
        except FileExistsError:
            flash('This file already exists', 'error')
        
    else:
        flash('Invalid!', 'error')
        
    return redirect(next)

