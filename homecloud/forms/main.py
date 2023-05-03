from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import Length, Regexp, DataRequired

class FileUploadForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next = kwargs.pop('next', None)
    
    @property 
    def nxt(self):
        return self.next
    
    file = FileField(
        'Archivo', 
        validators=[FileRequired()]
    )
    
    next = HiddenField(default=nxt, name='next', id='next')
    submit = SubmitField('Subir archivo')
    
class CreateDirForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next = kwargs.pop('next', None)
       
    @property 
    def nxt(self):
        return self.next
    
    dir = StringField(
        'Nombre del directorio', 
        validators=[ Length(1, 20), Regexp(r"^[\w.@+ -]+\Z"), DataRequired()],
        render_kw={'placeholder': 'Nombre del directorio'}
    )
    
    next = HiddenField(default=nxt, name='next', id='next')
    submit = SubmitField('Crear directorio')
    
class DeleteFileForm(FlaskForm):
    submit = SubmitField('Eliminar archivo')
    
class RenameForm(FlaskForm):
    name = StringField(
        'Nombre', 
        validators=[ Length(1, 20), Regexp(r"^[\w.@+ -]+\Z"), DataRequired()],
        render_kw={'placeholder': 'Nombre'}
    )
    
    submit = SubmitField('Renombrar')
    