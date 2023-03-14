from flask import Flask

def create_app(debug=True):
    app = Flask(__name__)
    
    from .config import DevelopmentConfig
    app.config.from_object(DevelopmentConfig())
    
    from .main import main_bp
    app.register_blueprint(main_bp)

    
    return app
