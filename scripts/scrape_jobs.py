import os
import sys
import logging
from datetime import datetime
import click

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.utils.job_scraper import JobScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/scraping.log'),
        logging.StreamHandler()
    ]
)

@click.command()
@click.option('--keywords', '-k', default='software engineer,data scientist,full stack developer', 
              help='Comma-separated job keywords to search for')
@click.option('--location', '-l', default='United States', help='Job location')
@click.option('--jobs-per-source', '-n', default=10, help='Number of jobs to fetch per source')
def scrape_jobs(keywords, location, jobs_per_source):
    """Scrape jobs from LinkedIn and save to database."""
    logger = logging.getLogger(__name__)
    logger.info(f"Starting LinkedIn job scraping for: {keywords} in {location}")
    
    app = create_app()
    with app.app_context():
        try:
            scraper = JobScraper()
            total_jobs = 0
            
            # Split keywords and scrape for each keyword combination
            for keyword in keywords.split(','):
                keyword = keyword.strip()
                logger.info(f"Searching for: {keyword}")
                
                jobs = scraper.scrape_all_sources(
                    keywords=keyword,
                    location=location,
                    num_jobs=jobs_per_source
                )
                
                # Save jobs to database
                from app.utils.db_utils import get_db
                db = get_db()
                
                for job in jobs:
                    try:
                        db.execute('''
                            INSERT INTO jobs (title, company, description, location, 
                                           application_link, posted_date, source)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT(application_link) DO NOTHING
                        ''', (
                            job['title'], job['company'], job['description'],
                            job['location'], job['application_link'],
                            job['posted_date'], job['source']
                        ))
                        total_jobs += 1
                    except Exception as e:
                        logger.error(f"Error saving job: {e}")
                        continue
                
                db.commit()
                logger.info(f"Saved {total_jobs} new jobs for keyword: {keyword}")
                
            logger.info(f"Scraping completed. Total new jobs saved: {total_jobs}")
            
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            raise

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    scrape_jobs()
