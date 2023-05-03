from flask import Flask, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_required

from homecloud.config import DevelopmentConfig

# create the extension
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    
    app.config.from_object(config_class)
    
    #initialization
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    
    register_blueprints(app)
    load_login_managers()
    load_index_view(app)
    
    with app.app_context():
        db.create_all()
    
    return app

def load_login_managers():
    from homecloud.models import User
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('auth_bp.login'))
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

def load_index_view(app):
    @app.route('/')
    @app.route('/index')
    @login_required
    def index():
        return redirect(url_for('main_bp.cloud_private'))
    
def register_blueprints(app):
    from homecloud.blueprints.main import main_bp
    app.register_blueprint(main_bp)
    
    from homecloud.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)
    
