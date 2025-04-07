from .linkedin_scraper import LinkedInScraper
from .glassdoor_scraper import GlassdoorScraper
from .indeed_scraper import IndeedScraper
from datetime import datetime, timedelta
import concurrent.futures

class JobScraper:
    def __init__(self):
        self.scrapers = {
            'linkedin': LinkedInScraper(),
            'glassdoor': GlassdoorScraper(),
            'indeed': IndeedScraper()
        }
    
    def scrape_all_sources(self, keywords, location, num_jobs=10):
        all_jobs = []
        
        # Use ThreadPoolExecutor to run scrapers concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.scrapers)) as executor:
            future_to_scraper = {
                executor.submit(scraper.scrape_jobs, keywords, location, num_jobs): name
                for name, scraper in self.scrapers.items()
            }
            
            for future in concurrent.futures.as_completed(future_to_scraper):
                scraper_name = future_to_scraper[future]
                try:
                    jobs = future.result()
                    print(f"Got {len(jobs)} jobs from {scraper_name}")
                    all_jobs.extend(jobs)
                except Exception as e:
                    print(f"{scraper_name} scraper failed: {e}")
        
        # Filter jobs to last 15 days
        cutoff_date = datetime.now() - timedelta(days=15)
        filtered_jobs = [
            job for job in all_jobs
            if datetime.strptime(job['posted_date'], '%Y-%m-%d') >= cutoff_date
        ]
        
        return filtered_jobs
