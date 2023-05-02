from flask import (
    Blueprint, 
    render_template, 
    redirect, 
    url_for, 
    flash
)

from flask_login.utils import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

from ..app import db
from ..models import User
from ..forms import LoginForm, RegisterForm, LogoutForm
from ..utils import not_logged_required

auth_bp = Blueprint('auth_bp', __name__,
                        template_folder='../templates/auth',
                        url_prefix='/auth',)

@auth_bp.route('/login', methods=['GET', 'POST'])
@not_logged_required
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user =  User.query.filter_by(email=form.email.data).first()
        
        login_user(user)
        flash('Has iniciado sesion correctamente')
        
        return redirect(url_for('main_bp.cloud_private'))
        
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
@not_logged_required
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
            flash('Este email o nombre de usuario ya esta en uso!', 'error')
            return redirect(url_for('auth_bp.register'))
        
        flash('Te has registrado correctamente. Ya puedes iniciar sesion!')
        
        return redirect(url_for('auth_bp.login'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    form = LogoutForm()
    
    if form.validate_on_submit():
        logout_user()
        flash('Has salido de la sesion satisfactoriamente')
                
        return redirect(url_for('auth_bp.login'))
        
    return render_template('logout.html', form=form)
