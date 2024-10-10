from flask import Blueprint

from .user_routes import user_routes
from .upload_routes import upload_routes

def register_routes(app):
    app.register_blueprint(user_routes)
    app.register_blueprint(upload_routes)
