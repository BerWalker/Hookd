# forms/auth_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models.user import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ], render_kw={'placeholder': 'Enter your email'})
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.')
    ], render_kw={'placeholder': 'Enter your password'})
    
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=4, max=25, message='Username must be between 4 and 25 characters.')
    ], render_kw={'placeholder': 'Choose a username'})
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ], render_kw={'placeholder': 'Enter your email'})
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=12, message='Password must be at least 8 characters long.')
    ], render_kw={'placeholder': 'Create a password'})
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password.'),
        EqualTo('password', message='Passwords must match.')
    ], render_kw={'placeholder': 'Confirm your password'})
    
    submit = SubmitField('Create Account')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email or log in.')
