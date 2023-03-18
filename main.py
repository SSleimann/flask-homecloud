import os

from flask import Blueprint, render_template, redirect, url_for, current_app, request

from werkzeug.utils import secure_filename

from . import db
from .models import User
from .utils import get_path_folders_and_files
from .forms import FileUploadForm, CreateDirForm

main_bp = Blueprint('main_bp', __name__,
                        template_folder='templates')

