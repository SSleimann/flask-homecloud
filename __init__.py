from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    from .config import DevelopmentConfig
    app.config.from_object(DevelopmentConfig())
    
    from .main import main_bp
    app.register_blueprint(main_bp)

    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app
