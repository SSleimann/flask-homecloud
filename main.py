import os

from flask import Blueprint, render_template, redirect, url_for, current_app

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from werkzeug.utils import secure_filename

main_bp = Blueprint('main_bp', __name__,
                        template_folder='templates')

class FileForm(FlaskForm):
    file = FileField(validators=[FileRequired()])

@main_bp.route('/')
def index():
    return 'HELLO WORLD'

@main_bp.route('/upload_file/<path:path>', methods=['GET', 'POST'])
def upload_file(path=None):
    
    form = FileForm()
    
    if form.validate_on_submit():
        f = form.file.data
        
        filename = secure_filename(f.filename)
        
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], path)
        
        if not os.path.exists(path):
            os.makedirs(path)
            
        f.save(os.path.join(path, filename))
        
        return redirect(url_for('main_bp.index'))
    
    return render_template('upload_file.html', form=form)