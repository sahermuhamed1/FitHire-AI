from .linkedin_scraper import LinkedInScraper
from datetime import datetime, timedelta

class JobScraper:
    def __init__(self):
        self.scraper = LinkedInScraper()
    
    def scrape_all_sources(self, keywords, location, num_jobs=10):
        try:
            jobs = self.scraper.scrape_jobs(keywords, location, num_jobs)
            print(f"Got {len(jobs)} jobs from LinkedIn")
            return jobs
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
            return []
