from flask_wtf import FlaskForm

from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import Length, Email, DataRequired, EqualTo, Regexp

from ..models import User

class LoginForm(FlaskForm):
    email = EmailField(
        'Email', 
        validators=[ Email(), DataRequired(), Length(1, 50) ]
    )
    
    password = PasswordField('Password', validators=[ DataRequired() ])
    submit = SubmitField('Log In')
    
    def validate(self, extra_validators=None):
        initial_validation = super().validate(extra_validators)
        
        if not initial_validation:
            return False
        
        user: User = User.query.filter_by(email=self.email.data).first()
        
        if not user:
            self.submit.errors.append("Invalid user or password")
            return False
        
        if not user.check_password(self.password.data):
            self.submit.errors.append("Invalid user or password")
            return False
        
        return True
    
class RegisterForm(FlaskForm):
    email = EmailField(
        'Email', 
        validators=[ Email(), DataRequired(), Length(1, 50) ]
    )
    
    password = PasswordField('Password', validators=[ DataRequired() ])
    password_confirmation = PasswordField(
        'Password confirmation', 
        validators=[ DataRequired(), EqualTo('password') ]
    )
    
    username = StringField('Username', validators=[DataRequired(), Length(1, 20), Regexp(r"^[\w.@+-]+\Z")])
    submit = SubmitField('Register')
    
