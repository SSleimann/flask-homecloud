import os

from werkzeug.utils import secure_filename

from flask import Blueprint, render_template, redirect, request, abort, flash
from flask_login.utils import login_required, current_user

from .utils import get_path_folders_and_files, is_own, get_user_path
from .forms import CreateDirForm, FileUploadForm

main_bp = Blueprint('main_bp', __name__,
                        template_folder='templates/main',
                        url_prefix='/main')

@main_bp.route('/cloud/private/', defaults={'path': ''})
@main_bp.route('/cloud/private/<path:path>')
@login_required
def cloud_private(path):
    _, dpath = get_user_path(path, 'private')
    
    try:
        files, folders = get_path_folders_and_files(dpath)
    except FileNotFoundError:
        abort(404, description='Carpeta no encontrada!')
    
    context = {
        'files': files,
        'folders': folders,
        'req': request,
        'usr': current_user,
        'form_create_dir': CreateDirForm(next=request.full_path),
        'form_upload_file': FileUploadForm(next=request.full_path),
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
        abort(404, description='Carpeta no conseguida!')
    
    next = request.full_path
    
    context = {
        'files': files,
        'folders': folders,
        'req': request,
        'usr': user,
        'form_create_dir': CreateDirForm(next=request.full_path),
        'form_upload_file': FileUploadForm(next=request.full_path),
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
        
        user, dpath = get_user_path(path, status.lower())
        is_own(user)
        
        new_dir_path = os.path.join(dpath, form.dir.data, '')
        
        try:
            os.mkdir(new_dir_path)
            flash('El directorio se creo con exito')
        except FileExistsError:
            flash('Este archivo ya existe', 'error')
        
    else:
        flash('Invalido!', 'error')
        
    return redirect(next)

@main_bp.route('/cloud/upload_file/', defaults={'path': ''}, methods=['POST'])
@main_bp.route('/cloud/upload_file/<path:path>', methods=['POST'])
@login_required
def cloud_upload_file(path):
    form = FileUploadForm()
    next = request.form.get('next', None)
    
    if next is None:
        abort(400)
    
    if form.validate_on_submit():
        file = request.files['file']
        filename = secure_filename(file.filename)
        
        status, path = path.split('/', maxsplit=1)
        user, dpath = get_user_path(path, status.lower())
        
        fpath = os.path.join(dpath, filename)
        is_own(user)
        
        file.save(fpath)
        flash('Se ha subido con exito el archivo!')
        
    else:
        flash('Invalido!', 'error')
        
    return redirect(next)