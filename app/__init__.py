import os
import logging
from flask import Flask
from flask_session import Session
from flask_cors import CORS
from flask_login import LoginManager

def create_app(config_class=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Load default configuration
    app.config.from_object('config.Config')
    
    # Override with passed config if any
    if config_class is not None:
        app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app)
    
    # Initialize Flask-Session
    Session(app)
    
    # Configure file upload settings
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Ensure instance path exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Ensure database directory exists
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)

    # Create required directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('app/uploads', exist_ok=True)
    os.makedirs('instance', exist_ok=True) # to hold the SQLite database 
    
    # Copy schema.sql to app directory if it doesn't exist
    schema_path = os.path.join(app.root_path, 'schema.sql')
    if not os.path.exists(schema_path): # If the schema file doesn't exist, create it
        with open(schema_path, 'w') as f:
            f.write('''
DROP TABLE IF EXISTS jobs;
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT,
    skills_required TEXT,
    application_link TEXT UNIQUE NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    posted_date TEXT NOT NULL,
    source TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs(source);
CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs(posted_date);
            '''.strip())

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.utils.db_utils import get_db
        from app.models.user import User
        db = get_db()
        return User.get_by_id(int(user_id), db)
    
    # Initialize database
    from app.utils import db_utils
    db_utils.init_app(app)
    
    # Register routes
    from app import routes
    app.register_blueprint(routes.bp)
    
    # Register auth blueprint
    from app import auth
    app.register_blueprint(auth.bp)
    
    return app