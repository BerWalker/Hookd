# services/auth_service.py
from models.user import User
from extensions import db, bcrypt
from datetime import datetime

class AuthService:
    @staticmethod
    def create_user(username, email, password):
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            raise ValueError('Email address already registered.')
        
        if User.query.filter_by(username=username).first():
            raise ValueError('Username already taken.')
        
        # Create new user
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.is_active and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return None
    
    @staticmethod
    def update_last_login(user):
        user.last_login = datetime.utcnow()
        db.session.commit()