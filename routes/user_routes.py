from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, db  # Import the User model and the database instance

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password
        hashed_password = generate_password_hash(password)  # Use Werkzeug's security functions
        
        # Store user data in the database
        user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(user)  # Add user to the session
        db.session.commit()    # Commit the session to save changes
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('user_routes.login'))  # Reference the correct route
    
    return render_template('register.html')

@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):  # Check password securely
            login_user(user)
            return redirect(url_for('user_routes.dashboard'))  # Reference the correct route
            
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@user_routes.route('/logout')
def logout():
    logout_user()  # Log the user out
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))  # Redirect to the homepage, reference 'main' blueprint if needed

@user_routes.route('/account', methods=['GET', 'POST'])
@login_required  # Protect this route
def account():
    user = current_user
    if request.method == 'POST':
        # Update user details if form is submitted
        username = request.form['username']
        email = request.form['email']

        user.username = username
        user.email = email
        db.session.commit()

        flash('Account details updated successfully!', 'success')
        return redirect(url_for('user_routes.account'))  # Reference the correct route

    return render_template('account.html', user=user)

@user_routes.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # Here you would generate a token and send it via email
            flash('A password reset link has been sent to your email.', 'success')
        else:
            flash('Email not found.', 'danger')
    
    return render_template('reset_password.html')

@user_routes.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    # Verify the token and get the user
    user = verify_reset_token(token)  # Implement this function to verify the token
    if user is None:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('user_routes.reset_password'))  # Reference the correct route

    if request.method == 'POST':
        new_password = request.form['new_password']
        hashed_password = generate_password_hash(new_password)  # Hash the new password
        user.password_hash = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('user_routes.login'))  # Reference the correct route

    return render_template('reset_password_confirm.html')  # Create a form for password entry
