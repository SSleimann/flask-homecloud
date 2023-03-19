from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

# create the extension
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    from .config import DevelopmentConfig
    app.config.from_object(DevelopmentConfig())
    
    #initialization
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    
    from .main import main_bp
    app.register_blueprint(main_bp)
    
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    with app.app_context():
        db.create_all()
    
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app
