# controllers/main_controller.py
from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
from utils.security import safe_redirect

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return safe_redirect(None, url_for('main.dashboard'))
    return safe_redirect(None, url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html', title='Dashboard')