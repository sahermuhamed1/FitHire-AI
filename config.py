import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/jobs.db')
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/app.log')
    JOBS_REFRESH_INTERVAL = timedelta(hours=6)
    MAX_JOBS_PER_SOURCE = 50
    REQUEST_TIMEOUT = 30
    RATE_LIMIT = "200/hour"
    
    # Add Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Add upload folder configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE = ':memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}