from flask_wtf import FlaskForm

from wtforms import EmailField, PasswordField, SubmitField, StringField, HiddenField
from wtforms.validators import Length, Email, DataRequired, EqualTo, Regexp

from homecloud.models import User

class LogoutForm(FlaskForm):
    logout = HiddenField(id='logout', default='_logout')
    
    submit = SubmitField('Salir de la sesión')
    
    def validate(self, extra_validators=None):
        initial_validation = super().validate(extra_validators)
        
        if not initial_validation:
            return False
        
        if not self.logout.data == '_logout':
            return False
        
        return True

class LoginForm(FlaskForm):
    email = EmailField(
        'Email', 
        validators=[ Email(), DataRequired(), Length(1, 50) ],
        render_kw={'placeholder': 'Email'}
    )
    
    password = PasswordField(
        'Clave', 
        validators=[ DataRequired() ],
        render_kw={'placeholder': 'Clave'}
    )
    
    submit = SubmitField('Iniciar sesión')
    
    def validate(self, extra_validators=None):
        initial_validation = super().validate(extra_validators)
        
        if not initial_validation:
            return False
        
        user: User = User.query.filter_by(email=self.email.data).first()
        
        if not user:
            self.submit.errors.append("Email o clave invalido")
            return False
        
        if not user.check_password(self.password.data):
            self.submit.errors.append("Email o clave invalido")
            return False
        
        return True
    
class RegisterForm(FlaskForm):
    email = EmailField(
        'Email', 
        validators=[ Email(), DataRequired(), Length(1, 50) ],
        render_kw={'placeholder': 'Email'}
    )
    
    password = PasswordField(
        'Clave', 
        validators=[ DataRequired() ],
        render_kw={'placeholder': 'Clave'}
    )
    
    password_confirmation = PasswordField(
        'Confirmacion de clave', 
        validators=[ DataRequired(), EqualTo('password') ],
        render_kw={'placeholder': 'Confirmacion de clave'}
    )
    
    username = StringField(
        'Nombre de usuario', 
        validators=[DataRequired(), Length(1, 20), Regexp(r"^[\w.@+-]+\Z")],
        render_kw={'placeholder': 'Nombre de usuario'}
    )
    
    submit = SubmitField('Registrar')
    
