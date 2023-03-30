from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms import StringField, SubmitField
from wtforms.validators import Length, Regexp, DataRequired

class FileUploadForm(FlaskForm):
    file = FileField('Upload a file', validators=[FileRequired()])
    submit = SubmitField('Submit')
    
class CreateDirForm(FlaskForm):
    dir = StringField('Directory name', validators=[ Length(1, 20), Regexp(r"^[\w.@+-]+\Z"), DataRequired()])
    submit = SubmitField('Submit')
    
