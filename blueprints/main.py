import os
import shutil

from werkzeug.utils import secure_filename

from flask import Blueprint, render_template, redirect, request, abort, flash, url_for, send_from_directory
from flask_login.utils import login_required, current_user

from ..utils import get_path_files_and_folders, is_own, get_user_path, protected_path
from ..forms import CreateDirForm, FileUploadForm, DeleteFileForm, RenameForm
from ..models import User
from ..app import db

main_bp = Blueprint('main_bp', __name__,
                        template_folder='../templates/main',
                        url_prefix='/main')

@main_bp.route('/cloud/public/', methods=['GET'])
@login_required
def cloud_public_redirect():
    return redirect(url_for('main_bp.cloud_public', username=current_user.username))

@main_bp.route('/cloud/private/', defaults={'path': '' })
@main_bp.route('/cloud/private/<path:path>')
@login_required
@protected_path
def cloud_private(path, encpath):
    dpath = os.path.join(current_user.get_private_user_path(), path)
    
    try:
        files, folders = get_path_files_and_folders(dpath)
    except FileNotFoundError:
        abort(404, description='Carpeta no encontrada!')
    
    context = {
        'files': files,
        'folders': folders,
        'req': request,
        'user': current_user,
        'curr_user': current_user,
        'form_create_dir': CreateDirForm(next=request.full_path),
        'form_upload_file': FileUploadForm(next=request.full_path),
        'path': encpath,
        'status': 'private'
    }
    
    return render_template('cloud.html', **context)

@main_bp.route('/cloud/public/<username>/path/', defaults={'path': ''}, methods=['GET', 'POST'])
@main_bp.route('/cloud/public/<username>/path/<path:path>', methods=['GET', 'POST'])
@login_required
@protected_path
def cloud_public(username, path, encpath):
    user = db.one_or_404(db.select(User).filter_by(username=username))
    
    dpath = os.path.join(user.get_public_user_path(), path)
    
    try:
        files, folders = get_path_files_and_folders(dpath)
    except FileNotFoundError:
        abort(404, description='Carpeta no conseguida!')
    
    context = {
        'files': files,
        'folders': folders,
        'req': request,
        'user': user,
        'curr_user': current_user,
        'form_create_dir': CreateDirForm(next=request.full_path),
        'form_upload_file': FileUploadForm(next=request.full_path),
        'path': encpath,
        'status': 'public'
    }
    
    return render_template('cloud.html', **context)

@main_bp.route('/cloud/create_dir/<status>/<username>/path/', defaults={'path': ''}, methods=['POST'])
@main_bp.route('/cloud/create_dir/<status>/<username>/<path:path>', methods=['POST'])
@login_required
@protected_path
def cloud_create_dir(status, username, path, encpath):
    form = CreateDirForm()
    next = request.form.get('next', None)
    
    user = db.one_or_404(db.select(User).filter_by(username=username), description='User not found!')
    is_own(user)
    
    if not status in ['private', 'public']:
        abort(404)
    
    if next is None:
        abort(400)
        
    if form.validate_on_submit():
        dpath = get_user_path(user, status, path)
        new_dir_path = os.path.join(dpath, form.dir.data, '')
        
        try:
            os.mkdir(new_dir_path)
            flash('El directorio se creo con exito')
        except FileExistsError:
            flash('Este archivo ya existe', 'error')
            
    else:
        flash('Invalido!', 'error')
        
    return redirect(next)

@main_bp.route('/cloud/upload_file/<status>/<username>/path/', defaults={'path': ''}, methods=['POST'])
@main_bp.route('/cloud/upload_file/<status>/<username>/path/<path:path>', methods=['POST'])
@login_required
@protected_path
def cloud_upload_file(status, username, path, encpath):
    form = FileUploadForm()
    next = request.form.get('next', None)
    
    user = db.one_or_404(db.select(User).filter_by(username=username), description='User not found!')
    is_own(user)
        
    if not status in ['private', 'public']:
        abort(404)
            
    if next is None:
        abort(400)
    
    if form.validate_on_submit():
        dpath = get_user_path(user, status, path)
        
        file = form.file.data
        filename = secure_filename(file.filename)
        
        fpath = os.path.join(dpath, filename)
        
        file.save(fpath)
        flash('Se ha subido con exito el archivo!')
        
    else:
        flash('Invalido!', 'error')
        
    return redirect(next)

@main_bp.route('/cloud/delete_file/<status>/<username>/path/', defaults={'path': ''}, methods=['GET', 'POST'])
@main_bp.route('/cloud/delete_file/<status>/<username>/path/<path:path>', methods=['GET', 'POST'])
@login_required
@protected_path
def cloud_delete_fl_fld(status, username, path, encpath):
    form = DeleteFileForm()
    next = request.args.get('next', None)
    
    user = db.one_or_404(db.select(User).filter_by(username=username), description='User not found!')
    is_own(user)
        
    if not status in ['private', 'public']:
        abort(404)
            
    if next is None:
        next = url_for('main_bp.cloud_private') if status == 'private' else url_for('main_bp.cloud_public', username=user.username)
    
    if form.validate_on_submit():
        
        fpath = get_user_path(user, status, path)
        
        if os.path.isfile(fpath):
            try:
                os.remove(fpath)
                flash('Se ha eliminado con exito el archivo!')
            except FileNotFoundError:
                flash('Este archivo no existe!', 'error')
        
        else:
            try:
                shutil.rmtree(fpath)
                flash('Se ha eliminado con exito la carpeta!')
            except FileNotFoundError:
                flash('Esta carpeta no existe!', 'error')
                
        return redirect(next)
        
    return render_template('delete_file.html', form=form)

@main_bp.route('/cloud/download_file/<status>/<username>/path/', defaults={'path': ''})
@main_bp.route('/cloud/download_file/<status>/<username>/path/<path:path>')
@login_required
@protected_path
def cloud_download_file(status, username, path, encpath):
    user = db.one_or_404(db.select(User).filter_by(username=username), description='User not found!')
    
    if not status in ['private', 'public']:
         abort(404)
    
    if status == 'private' and current_user.email != user.email:
        abort(404, description='Este archivo no existe')
        
    dpath = get_user_path(user, status, path)
    
    filename = os.path.basename(dpath)
    fpath = os.path.dirname(dpath)
    
    if not os.path.exists(fpath):
        abort(404, description='Este archivo no existe')
    
    return send_from_directory(fpath, filename, as_attachment=True)

@main_bp.route('/cloud/rename/<status>/<username>/path/', defaults={'path': ''}, methods=['GET', 'POST'])
@main_bp.route('/cloud/rename/<status>/<username>/path/<path:path>', methods=['GET', 'POST'])
@login_required
@protected_path
def cloud_rename_fl_fld(status, username, path, encpath):
    form = RenameForm()
    next = request.args.get('next', None)
    
    user = db.one_or_404(db.select(User).filter_by(username=username), description='User not found!')
    is_own(user)
    
    if next is None:
        next = url_for('main_bp.cloud_private') if status == 'private' else url_for('main_bp.cloud_public', username=user.username)
    
    if not status in ['private', 'public']:
         abort(404)
    
    if form.validate_on_submit():
        user_path = get_user_path(user, status, path)
        dir_name = os.path.dirname(user_path)
        
        try:
            os.rename(user_path, os.path.join(dir_name, form.name.data))
            flash('Se ha renombrado con exito!')
        except FileNotFoundError:
            flash('Este archivo no existe!', 'error')
        
        return redirect(next)
        
    return render_template('cloud_rename.html', form=form)