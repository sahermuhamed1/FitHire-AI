import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import os
from datetime import datetime, timedelta
from .job_scraper import JobScraper
from werkzeug.security import generate_password_hash

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Initialize the database."""
    db = get_db()
    
    try:
        # Read schema from file
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
            
        # Add sample jobs if none exist
        if not db.execute('SELECT 1 FROM jobs LIMIT 1').fetchone():
            add_fallback_sample_jobs(db)
            
        db.commit()
        current_app.logger.info("Database initialized successfully")
    except Exception as e:
        current_app.logger.error(f"Error initializing database: {e}")
        db.rollback()
        raise

def get_filtered_jobs(source=None, days=None):
    """Get jobs filtered by source and/or date range."""
    db = get_db()
    query = 'SELECT * FROM jobs WHERE 1=1'
    params = []
    
    if source:
        query += ' AND source = ?'
        params.append(source)
    
    if days:
        query += ' AND date(posted_date) >= date("now", "-? days")'
        params.append(days)
    
    query += ' ORDER BY posted_date DESC'
    
    return db.execute(query, params).fetchall()

def add_sample_jobs(db):
    current_date = datetime.now()
    date_15_days_ago = current_date - timedelta(days=15)
    
    try:
        # Use the new job scraper
        scraper = JobScraper()
        jobs = scraper.scrape_all_sources(
            keywords="software engineer OR data scientist OR developer",
            location="United States",
            num_jobs=20
        )
        
        # Insert jobs
        for job in jobs:
            if all([job.get('title'), job.get('company'), job.get('description'), job.get('application_link')]):
                db.execute(
                    'INSERT INTO jobs (title, company, description, location, application_link, posted_date, source)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (job['title'], job['company'], job['description'], 
                     job['location'], job['application_link'], job['posted_date'], job['source'])
                )
        db.commit()
        print(f"Added {len(jobs)} jobs from multiple sources")
            
    except Exception as e:
        print(f"Error adding jobs: {e}")
        add_fallback_sample_jobs(db)

def add_fallback_sample_jobs(db):
    def generate_search_link(title, company):
        # Create a search-friendly URL
        search_query = f"{title} {company}".replace(' ', '%20')
        return f"https://www.linkedin.com/jobs/search/?keywords={search_query}"

    sample_jobs = [
        ('Software Engineer', 'TechCorp Inc.', 'We are looking for an experienced software engineer familiar with Python, Flask, and SQL. The candidate should have strong problem-solving skills and be able to work in a team environment.', 'San Francisco, CA', 'Python, Flask, SQL, Git', None),
        ('Data Scientist', 'DataAnalytics Co.', 'Seeking a data scientist with expertise in machine learning and natural language processing. The ideal candidate will have experience with Python, PyTorch, and SQL.', 'Remote', 'Python, ML, NLP, PyTorch, SQL', None),
        ('Full Stack Developer', 'WebSolutions LLC', 'Looking for a full stack developer with experience in React and Node.js. Should be familiar with modern web development practices and RESTful APIs.', 'New York, NY', 'JavaScript, React, Node.js, Express, MongoDB', None),
        ('DevOps Engineer', 'CloudTech Systems', 'Seeking a DevOps engineer to help manage our cloud infrastructure. Experience with AWS, Docker, and Kubernetes is required.', 'Seattle, WA', 'AWS, Docker, Kubernetes, Terraform, Linux', None),
        ('UI/UX Designer', 'CreativeWorks Agency', 'Looking for a talented UI/UX designer to create beautiful and intuitive user interfaces. Experience with Figma and Adobe Creative Suite is a plus.', 'Los Angeles, CA', 'UI/UX, Figma, Adobe XD, Photoshop, Illustrator', None)
    ]
    
    for job in sample_jobs:
        title, company, description, location, skills, _ = job
        # Generate a search link if no direct link is provided
        search_link = generate_search_link(title, company)
        
        db.execute(
            'INSERT INTO jobs (title, company, description, location, skills_required, application_link, posted_date, source)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (title, company, description, location, skills, search_link, 
             datetime.now().strftime('%Y-%m-%d'), 'sample')
        )
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('reset-admin')
@click.option('--password', default='admin123', help='New admin password')
@with_appcontext
def reset_admin_command(password):
    """Reset the admin password."""
    db = get_db()
    password_hash = generate_password_hash(password)
    
    try:
        # Check if admin exists
        admin = db.execute('SELECT 1 FROM users WHERE username = ?', ('admin',)).fetchone()
        
        if admin:
            # Update existing admin
            db.execute('UPDATE users SET password_hash = ? WHERE username = ?', 
                      (password_hash, 'admin'))
            click.echo(f'Admin password updated. Username: admin, Password: {password}')
        else:
            # Create new admin
            db.execute(
                'INSERT INTO users (username, email, password_hash, is_admin) VALUES (?, ?, ?, ?)',
                ('admin', 'admin@fithire.com', password_hash, 1)
            )
            click.echo(f'Admin user created. Username: admin, Password: {password}')
        
        db.commit()
    except Exception as e:
        click.echo(f'Error resetting admin password: {e}')
        db.rollback()

def verify_db_tables():
    """Verify that required tables exist or reinitialize if they don't."""
    db = get_db()
    try:
        # Check if essential tables exist
        db.execute('SELECT 1 FROM users LIMIT 1')
        db.execute('SELECT 1 FROM jobs LIMIT 1')
        return True
    except sqlite3.OperationalError:
        # Tables don't exist, initialize database
        init_db()
        return False

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(reset_admin_command)
    
    # Initialize database when app starts
    with app.app_context():
        verify_db_tables()