import os
from datetime import timedelta

class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'jobs.db')
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_TYPE = 'filesystem'
    LOG_FILE = 'logs/app.log'

class DevelopmentConfig(Config):
    """Development config."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production config."""
    DEBUG = False
    TESTING = False
    # In production, set SECRET_KEY from environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')

class TestingConfig(Config):
    """Testing config."""
    TESTING = True
    DEBUG = True
    # Use separate test database
    DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'test.db')

# Config dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}