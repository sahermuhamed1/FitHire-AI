import os
from app import create_app
from config import config
import logging
from logging.handlers import RotatingFileHandler
import click

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
        
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=10240,
        backupCount=10
    )
    
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('FitHire AI startup')

@click.command()
@click.option('--env', default='development', 
              type=click.Choice(['development', 'production', 'testing']),
              help='The environment to run the application in')
def run(env):
    """Run the application with the specified environment."""
    app = create_app(config[env])
    setup_logging(app)
    
    if env == 'production':
        from waitress import serve
        app.logger.info('Starting production server...')
        serve(app, host='0.0.0.0', port=8000)
    else:
        app.logger.info('Starting development server...')
        app.run(debug=True)

if __name__ == '__main__':
    run()