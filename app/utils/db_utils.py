import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import os
from datetime import datetime, timedelta
from .job_scraper import JobScraper

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
    try:
        db = get_db()
        
        # Read schema from file
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
        
        # Add sample job data
        try:
            add_sample_jobs(db)
        except Exception as e:
            print(f"Warning: Could not add sample jobs: {e}")
            # Fallback to sample data if scraping fails
            add_fallback_sample_jobs(db)
            
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
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
        # Keep your existing job data tuples but add None for application_link
        ('Software Engineer', 'TechCorp Inc.', 'We are looking for...', 'San Francisco, CA', 'Python, Flask, SQL, Git', None),
        ('Data Scientist', 'DataAnalytics Co.', 'Seeking a data scientist...', 'Remote', 'Python, ML, NLP, PyTorch, SQL', None),
        # ... rest of your sample jobs ...
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

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)