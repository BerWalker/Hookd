# app.py
from dotenv import load_dotenv
import time
import psycopg2
from sqlalchemy.exc import OperationalError

load_dotenv()

from flask import Flask
from config import Config
from extensions import db, login_manager, bcrypt, mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from controllers.main_controller import main_bp
    app.register_blueprint(main_bp)
    
    from controllers.health_controller import health_bp
    app.register_blueprint(health_bp)
    
    from models.user import load_user
    login_manager.user_loader(load_user)
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)