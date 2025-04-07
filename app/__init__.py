import os
from flask import Flask
from config import Config
from flask_session import Session

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config.from_object(Config)
    
    if test_config:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register routes
    from app import routes
    app.register_blueprint(routes.bp)
    
    # Add URL rule for the index page
    app.add_url_rule('/', endpoint='index')
    
    # Initialize database
    from app.utils import db_utils
    db_utils.init_app(app)
    
    # Initialize Flask-Session
    Session(app)
    
    return app