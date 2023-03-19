from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms import StringField
from wtforms.validators import Length

class FileUploadForm(FlaskForm):
    file = FileField('Upload a file', FileRequired())

class CreateDirForm(FlaskForm):
    dir = StringField('Directory name', Length(1, 20))
    
