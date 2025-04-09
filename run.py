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
@click.option('--reset-admin', is_flag=True, help='Reset admin password')
@click.option('--admin-password', default='admin123', help='New admin password when using --reset-admin')
def run(env, reset_admin, admin_password):
    """Run the application with the specified environment."""
    config_class = config[env]
    app = create_app(config_class)
    setup_logging(app)
    
    # Initialize database on startup
    with app.app_context():
        from app.utils.db_utils import init_db
        try:
            init_db()
            app.logger.info('Database initialized successfully')
            
            # Reset admin if requested
            if reset_admin:
                from werkzeug.security import generate_password_hash
                from app.utils.db_utils import get_db
                db = get_db()
                password_hash = generate_password_hash(admin_password)
                
                # Check if admin exists
                admin = db.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
                
                if admin:
                    # Update existing admin
                    db.execute('UPDATE users SET password_hash = ? WHERE username = ?', 
                              (password_hash, 'admin'))
                    app.logger.info(f'Admin password updated to: {admin_password}')
                else:
                    # Create new admin
                    db.execute(
                        'INSERT INTO users (username, email, password_hash, is_admin) VALUES (?, ?, ?, ?)',
                        ('admin', 'admin@fithire.com', password_hash, 1)
                    )
                    app.logger.info(f'Admin user created with password: {admin_password}')
                
                db.commit()
                click.echo(f"Admin user reset. You can login with username 'admin' and password '{admin_password}'")
                
        except Exception as e:
            app.logger.error(f'Error initializing database: {e}')
    
    if env == 'production':
        from waitress import serve
        app.logger.info('Starting production server...')
        serve(app, host='0.0.0.0', port=8000)
    else:
        app.logger.info('Starting development server...')
        app.run(debug=True)

if __name__ == '__main__':
    run()