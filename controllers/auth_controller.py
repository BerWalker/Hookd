# controllers/auth_controller.py
from flask import Blueprint, render_template, url_for, flash, request, redirect
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from services.auth_service import AuthService
from forms.auth_form import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from extensions import db
from utils.security import safe_redirect

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return safe_redirect(None, url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = AuthService.authenticate_user(form.email.data, form.password.data)
        if user:
            login_user(user, remember=form.remember_me.data)
            AuthService.update_last_login(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return safe_redirect(next_page, url_for('main.dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('auth/login.html', form=form, title='Login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return safe_redirect(None, url_for('main.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = AuthService.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            flash('Account created successfully! Please log in.', 'success')
            return safe_redirect(None, url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'error')
    
    return render_template('auth/register.html', form=form, title='Create Account')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return safe_redirect(None, url_for('main.dashboard'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if AuthService.send_password_reset_email(user):
                flash('Password reset instructions have been sent to your email address.', 'success')
            else:
                flash('Failed to send reset email. Please try again later.', 'error')
        else:
            flash('If an account with that email exists, password reset instructions have been sent.', 'success')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', form=form, title='Forgot Password')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return safe_redirect(None, url_for('main.dashboard'))
    
    user = AuthService.verify_reset_token(token)
    if not user:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if AuthService.reset_password(token, form.password.data):
            flash('Your password has been reset successfully. You can now log in with your new password.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Failed to reset password. Please try again.', 'error')
    
    return render_template('auth/reset_password.html', form=form, title='Reset Password')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))