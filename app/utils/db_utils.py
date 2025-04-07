import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import os
from datetime import datetime, timedelta

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
    from app.utils.linkedin_scraper import LinkedInScraper
    from app.utils.indeed_scraper import IndeedScraper
    from app.utils.glassdoor_scraper import GlassdoorScraper
    
    current_date = datetime.now()
    date_45_days_ago = current_date - timedelta(days=45)
    
    scrapers = [
        LinkedInScraper(),
        IndeedScraper(),
        GlassdoorScraper()
    ]
    
    try:
        all_jobs = []
        for scraper in scrapers:
            try:
                jobs = scraper.scrape_jobs(
                    keywords="software engineer OR data scientist OR developer",
                    location="United States",
                    num_jobs=20  # Reduced per source to avoid overwhelming
                )
                # Only add jobs that have valid application links
                valid_jobs = [job for job in jobs if job.get('application_link')]
                all_jobs.extend(valid_jobs)
                time.sleep(2)  # Pause between different sources
            except Exception as e:
                print(f"Error with {scraper.__class__.__name__}: {e}")
                continue
        
        # Filter and insert scraped jobs within last 45 days
        for job in all_jobs:
            job_date = datetime.strptime(job.get('posted_date', current_date.strftime('%Y-%m-%d')), '%Y-%m-%d')
            if job_date >= date_45_days_ago:
                db.execute(
                    'INSERT INTO jobs (title, company, description, location, application_link, posted_date, source)'
                    ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (job['title'], job['company'], job['description'], 
                     job['location'], job['application_link'], job_date.strftime('%Y-%m-%d'),
                     job.get('source', 'unknown'))
                )
        db.commit()
        print(f"Added valid jobs from multiple sources")
            
    except Exception as e:
        print(f"Error adding jobs: {e}")
        add_fallback_sample_jobs(db)
    
    # Add sample jobs with recent dates
    sample_jobs = [
        ('Software Engineer', 'TechCorp Inc.', 'We are looking for a software engineer with experience in Python, Flask, and SQL. The ideal candidate will have 3+ years of experience in web development and be comfortable working in a fast-paced environment.', 'San Francisco, CA', 'Python, Flask, SQL, Git'),
        ('Data Scientist', 'DataAnalytics Co.', 'Seeking a data scientist with strong background in machine learning, NLP, and data visualization. Must be proficient in Python, PyTorch or TensorFlow, and have experience with large datasets.', 'Remote', 'Python, ML, NLP, PyTorch, SQL'),
        ('Frontend Developer', 'WebUI Systems', 'Frontend developer needed for our growing team. Experience with React, TypeScript, and modern CSS frameworks required. Knowledge of UI/UX principles a plus.', 'Boston, MA', 'JavaScript, TypeScript, React, CSS, HTML'),
        ('DevOps Engineer', 'CloudNative Ltd', 'Looking for a DevOps engineer to help build and maintain our cloud infrastructure. Experience with AWS, Docker, and CI/CD pipelines is essential.', 'Seattle, WA', 'AWS, Docker, Kubernetes, CI/CD, Linux'),
        ('Product Manager', 'ProductSuite Inc.', 'Experienced product manager needed to lead development of our SaaS platform. Must have experience in agile methodologies and a technical background.', 'New York, NY', 'Agile, Jira, Product Development, SaaS'),
        ('Full Stack Developer', 'WebStack Solutions', 'Full stack developer needed with experience in Node.js and React. Should be comfortable with both frontend and backend development.', 'Austin, TX', 'JavaScript, Node.js, React, MongoDB, Express'),
        ('AI Research Engineer', 'AI Innovations', 'Research engineer needed for cutting-edge AI projects. PhD in machine learning or related field preferred. Experience with NLP models a plus.', 'Pittsburgh, PA', 'Python, PyTorch, NLP, Research'),
        ('UX/UI Designer', 'DesignThink Co.', 'Creative designer needed for our product team. Experience with Figma and Adobe suite required. Portfolio must demonstrate strong UI/UX skills.', 'Los Angeles, CA', 'Figma, Adobe XD, UI Design, User Research'),
        ('Mobile Developer', 'AppWorks Inc.', 'Looking for a mobile developer with experience in React Native or Flutter. Must be able to build and deploy cross-platform mobile applications.', 'Chicago, IL', 'React Native, Flutter, JavaScript, Mobile Development'),
        ('Machine Learning Engineer', 'ML Technologies', 'Machine learning engineer needed to develop and deploy ML models. Experience with Python, scikit-learn, and model deployment required.', 'Denver, CO', 'Python, scikit-learn, TensorFlow, ML Ops')
    ]
    
    # Distribute sample jobs over the last 45 days
    days_interval = 45 // len(sample_jobs)
    for i, job in enumerate(sample_jobs):
        job_date = current_date - timedelta(days=i*days_interval)
        db.execute(
            'INSERT INTO jobs (title, company, description, location, skills_required, posted_date)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            job + (job_date.strftime('%Y-%m-%d'),)
        )
    db.commit()

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