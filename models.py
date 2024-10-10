# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # Optional: Define the table name explicitly

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'  # Optional: Add a string representation

    # You may want to add methods for creating a user, checking passwords, etc.
    # Example:
    # def check_password(self, password):
    #     return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
