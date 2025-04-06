import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'ai_matcher.db')
    
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # Ensure instance directory exists
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance'), exist_ok=True)