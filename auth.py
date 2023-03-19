from flask import (
    Blueprint, 
    render_template, 
    redirect, 
    url_for, 
    abort, 
    request,
    flash
)
from flask_login.utils import login_user, logout_user

from sqlalchemy.exc import IntegrityError

from .models import User
from .forms import LoginForm, RegisterForm
from . import db

auth_bp = Blueprint('auth_bp', __name__,
                        template_folder='templates/auth',
                        url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user =  User.query.filter_by(email=form.email.data).first()
        
        login_user(user)
        flash('Login succesfully')
        
        return redirect(url_for('main_bp.index'))
        
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        
        user.set_password(form.password.data)
        
        db.session.add(user)
        
        try:
            db.session.commit()
            
        except IntegrityError:
            db.session.rollback()
            flash('This email or username already exists!')
            return redirect(url_for('auth_bp.register'))
        
        flash('Register succesfully. You can login!')
        
        return redirect(url_for('auth_bp.login'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        logout = request.form.get('logout', None)
        
        if not '_logout' == logout:
            abort(400, description="Invalid logout")
        
        logout_user()
        flash('Logout succesfully')
        
        return redirect(url_for('main_bp.index'))
        
    return render_template('logout.html')
