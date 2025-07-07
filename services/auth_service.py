# services/auth_service.py
from models.user import User
from extensions import db, bcrypt, mail
from datetime import datetime, timedelta
from flask import current_app, url_for
from flask_mail import Message

class AuthService:
    @staticmethod
    def create_user(username, email, password):
        if User.query.filter_by(email=email).first():
            raise ValueError('Email address already registered.')
        
        if User.query.filter_by(username=username).first():
            raise ValueError('Username already taken.')
        
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
    
    @staticmethod
    def send_password_reset_email(user):
        if not current_app.config.get('MAIL_SERVER') or not current_app.config.get('MAIL_USERNAME'):
            current_app.logger.error("Email configuration is missing. Please check MAIL_SERVER and MAIL_USERNAME settings.")
            return False
        
        try:
            token = user.generate_reset_token()
            db.session.commit()
            
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            
            msg = Message(
                'Password Reset Request',
                recipients=[user.email],
                body=f'''To reset your password, visit the following link:

{reset_url}

If you did not make this request, simply ignore this email and no changes will be made.

This link will expire in 1 hour.

Best regards,
Hookd Team'''
            )
            
            mail.send(msg)
            current_app.logger.info(f"Password reset email sent successfully to {user.email}")
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to send email to {user.email}: {str(e)}")
            db.session.rollback()
            return False
    
    @staticmethod
    def verify_reset_token(token):
        user = User.query.filter_by(reset_token=token).first()
        if user and user.reset_token_expires and user.reset_token_expires > datetime.utcnow():
            return user
        return None
    
    @staticmethod
    def reset_password(token, new_password):
        user = AuthService.verify_reset_token(token)
        if user:
            user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.clear_reset_token()
            db.session.commit()
            return user
        return None