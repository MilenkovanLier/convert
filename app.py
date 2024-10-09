from flask import Flask, request, render_template, send_file, session, jsonify  # Consolidated Flask imports

import os  # For operating system functionalities
import shutil  # For file operations
import uuid  # For generating unique folder names

from dotenv import load_dotenv  # For loading environment variables
from flask_session import Session  # For managing sessions
import redis  # For connecting to Redis
from flask_sqlalchemy import SQLAlchemy  # For SQLAlchemy ORM
from flask_migrate import Migrate  # For database migrations

from convert import convert_images_to_webp  # Custom import for image conversion function


load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    # User model with necessary attributes
    pass

@login_manager.user_loader
def load_user(user_id):
    # Fetch user from database
    return get_user_by_id(user_id)  # Implement this function to retrieve the user

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Store user data in database
        create_user(username, email, hashed_password)  # Implement this function
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            login_user(user)
            return redirect(url_for('dashboard'))  # Redirect to the dashboard
            
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()  # Log the user out
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))  # Redirect to the homepage

@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))

    return render_template('account.html', user=user)

@app.route('/reset_password', methods=['GET', 'POST'])
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

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    # Verify the token and get the user
    user = verify_reset_token(token)  # Implement this function to verify token
    if user is None:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('reset_password'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        user.password_hash = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password_confirm.html')  # Create a form for password entry


# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: to suppress warnings


# Create SQLAlchemy instance
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)


# Test Model (optional)
class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))



@app.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        # Attempt to query the database
        result = TestModel.query.all()
        return jsonify({'message': 'Connection successful!', 'data': [r.name for r in result]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Configure Redis for session storage
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'session:'
app.config['SESSION_REDIS'] = redis.Redis(host='localhost', port=6379)  # Connect to Redis

# Initialize the session object
Session(app)

# Set a secret key for sessions
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback_secret_key')

# Your existing routes go here

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_by_username(username)  # Implement this function
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
            login_user(user)
            return redirect(url_for('dashboard'))  # Redirect to a secure area
            
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html')


@app.route('/update_password', methods=['PUT'])
def update_password():
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')

    # Hash the new password
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    # Update user password in the database
    user = User.query.filter_by(username=username).first()
    if user:
        user.password = hashed_password
        db.session.commit()
        return jsonify({'message': 'Password updated successfully!'}), 200
    else:
        return jsonify({'message': 'User not found!'}), 404


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return "No file part", 400

    # Create a unique directory for the user's session
    user_id = str(uuid.uuid4())  # Generate a unique identifier
    user_upload_folder = os.path.join('uploads', user_id, 'PNG')
    user_converted_folder = os.path.join('uploads', user_id, 'WEBP')
    
    os.makedirs(user_upload_folder, exist_ok=True)
    os.makedirs(user_converted_folder, exist_ok=True)

    files = request.files.getlist('files[]')
    quality = int(request.form.get('quality', 80))
    converted_count = 0

    for file in files:
        if file and file.filename.endswith(('.png', '.tiff', '.tif', '.jpg', '.jpeg')):
            file_path = os.path.join(user_upload_folder, file.filename)
            file.save(file_path)

    converted_count = convert_images_to_webp(user_upload_folder, user_converted_folder, quality)

    download_link = f'/download/{user_id}'  # Create a unique download link
    return {'download_link': download_link, 'converted_count': converted_count}, 200

@app.route('/download/<user_id>')
def download_files(user_id):
    zip_file_path = f'converted_files_{user_id}.zip'
    user_converted_folder = os.path.join('uploads', user_id, 'WEBP')

    # Create a zip file from the converted folder
    shutil.make_archive(zip_file_path.replace('.zip', ''), 'zip', user_converted_folder)

    # Now delete all files in both the PNG and WEBP folders
    for folder in [os.path.join('uploads', user_id, 'PNG'), user_converted_folder]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    return send_file(zip_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application
