# app.py
from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from config import Config
from extensions import db, login_manager, bcrypt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from controllers.main_controller import main_bp
    app.register_blueprint(main_bp)
    
    # Register user loader
    from models.user import load_user
    login_manager.user_loader(load_user)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)