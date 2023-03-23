from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired

class FileUploadForm(FlaskForm):
    file = FileField('Upload a file', validators=[FileRequired()])

class CreateDirForm(FlaskForm):
    dir = StringField('Directory name', validators=[ Length(1, 20) ])
    
class SearchByUsernameForm(FlaskForm):
    username = StringField('Username', validators=[ Length(1, 20), DataRequired() ] )
    submit = SubmitField('Submit')
    
