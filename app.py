from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_login import LoginManager
from dotenv import load_dotenv
import os

from config import Config
from models import db, User
from routes.user_routes import user_routes
from routes.upload_routes import upload_routes

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback_secret_key')  # Set a secret key for the app

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_routes.login'  # Specify login route for @login_required

@login_manager.user_loader
def load_user(user_id):
    # Fetch user from the database by ID
    return User.query.get(user_id)

# Register blueprints for different functionalities
app.register_blueprint(user_routes)   # Handles user registration, login, account, and password reset
app.register_blueprint(upload_routes) # Handles image upload and conversion routes

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
