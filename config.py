import os
import redis

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Optional: to suppress warnings

    # Session configuration
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'session:'
    SESSION_REDIS = redis.Redis(host='localhost', port=6379)

    # Template auto-reload (to reflect changes in templates)
    TEMPLATES_AUTO_RELOAD = True
