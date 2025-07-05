# models/user.py
from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta
import secrets
import string

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Password reset fields
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expires = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def generate_reset_token(self):
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        self.reset_token = token
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        return token
    
    def clear_reset_token(self):
        self.reset_token = None
        self.reset_token_expires = None

def load_user(user_id):
    return User.query.get(int(user_id))