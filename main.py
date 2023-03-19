import os

from flask import Blueprint, render_template, redirect, url_for, current_app, request

from werkzeug.utils import secure_filename

from flask_login.utils import login_required

from . import db
from .models import User
from .utils import get_path_folders_and_files
from .forms import CreateDirForm, FileUploadForm

main_bp = Blueprint('main_bp', __name__,
                        template_folder='templates/main',
                        url_prefix='/main')


@main_bp.route('/')
@login_required
def index():
    return 'HELLOw'

