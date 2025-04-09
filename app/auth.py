import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils.db_utils import get_db
from app.models.user import User
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        db = get_db()
        error = None
        
        # Form validation
        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters long.'
        
        # Check if username or email already exists
        if error is None:
            if User.get_by_username(username, db):
                error = f"Username {username} is already taken."
            elif User.get_by_email(email, db):
                error = f"Email {email} is already registered."
        
        # Create new user
        if error is None:
            try:
                user = User.create(username, email, password)
                db.execute(
                    'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                    (user.username, user.email, user.password_hash)
                )
                db.commit()
                flash('Account created successfully. Please log in.', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                error = f"Error creating account: {e}"
        
        flash(error, 'danger')
    
    return render_template('auth/signup.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = 'remember' in request.form
        
        db = get_db()
        error = None
        
        # First try with email
        user = User.get_by_email(email, db)
        
        # If not found, try with username (for admin logins)
        if user is None:
            user = User.get_by_username(email, db)
        
        if user is None:
            error = 'Incorrect email or username.'
        elif not user.check_password(password):
            error = 'Incorrect password.'
        
        if error is None:
            # Use Flask-Login to handle session
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            
            # Redirect admins to admin panel
            if user.is_admin:
                return redirect(next_page or url_for('main.upload_jobs'))
            
            return redirect(next_page or url_for('main.index'))
        
        flash(error, 'danger')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

# Function to check if current user is admin
def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You must be an admin to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view