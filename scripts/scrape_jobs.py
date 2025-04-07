import os
import sys
import logging
from datetime import datetime

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.utils.linkedin_scraper import LinkedInScraper
from app.utils.db_utils import get_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)

def scrape_and_save_jobs():
    logger = logging.getLogger(__name__)
    logger.info("Starting job scraping process")
    
    app = create_app()
    with app.app_context():
        try:
            # Initialize scraper
            scraper = LinkedInScraper()
            
            # Define search parameters
            search_queries = [
                {"keywords": "software engineer", "location": "United States"},
                {"keywords": "data scientist", "location": "United States"},
                {"keywords": "full stack developer", "location": "United States"}
            ]
            
            total_jobs = 0
            db = get_db()
            
            for query in search_queries:
                logger.info(f"Searching for: {query['keywords']} in {query['location']}")
                
                jobs = scraper.scrape_jobs(
                    keywords=query['keywords'],
                    location=query['location'],
                    num_jobs=20  # Fetch 20 jobs per query to get 60 total
                )
                
                # Insert jobs into database
                for job in jobs:
                    try:
                        db.execute('''
                            INSERT INTO jobs (title, company, description, location, application_link, created)
                            VALUES (?, ?, ?, ?, ?, ?)
                            ON CONFLICT(application_link) DO NOTHING
                        ''', (
                            job['title'],
                            job['company'],
                            job['description'],
                            job['location'],
                            job['application_link'],
                            datetime.now()
                        ))
                        total_jobs += 1
                    except Exception as e:
                        logger.error(f"Error inserting job: {e}")
                        continue
                
                db.commit()
                logger.info(f"Saved {len(jobs)} jobs from current query")
            
            logger.info(f"Scraping completed. Total jobs saved: {total_jobs}")
            
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            raise

if __name__ == "__main__":
    scrape_and_save_jobs()
