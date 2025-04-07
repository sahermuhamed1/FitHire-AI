import requests
from bs4 import BeautifulSoup
import time
from random import randint
import logging

class LinkedInScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = "https://www.linkedin.com/jobs/search"
        self.logger = logging.getLogger(__name__)

    def scrape_jobs(self, keywords, location="", num_jobs=50):
        jobs = []
        page = 0
        retries = 3
        
        while len(jobs) < num_jobs:
            try:
                params = {
                    'keywords': keywords,
                    'location': location,
                    'start': page * 25,
                    'f_TPR': 'r86400'  # Last 24 hours
                }
                
                # Implement retry mechanism
                for attempt in range(retries):
                    try:
                        response = requests.get(self.base_url, headers=self.headers, params=params, timeout=10)
                        response.raise_for_status()
                        break
                    except requests.RequestException as e:
                        if attempt == retries - 1:
                            self.logger.error(f"Failed to fetch page after {retries} attempts: {e}")
                            return jobs
                        time.sleep(randint(2, 5))
                
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='base-card')
                
                if not job_cards:
                    self.logger.info("No more job cards found")
                    break
                
                for card in job_cards:
                    if len(jobs) >= num_jobs:
                        break
                        
                    try:
                        title = card.find('h3', class_='base-search-card__title').text.strip()
                        company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                        location = card.find('span', class_='job-search-card__location').text.strip()
                        link = card.find('a', class_='base-card__full-link').get('href').split('?')[0]
                        
                        # Get detailed job description
                        job_response = requests.get(link, headers=self.headers)
                        job_soup = BeautifulSoup(job_response.text, 'html.parser')
                        description = job_soup.find('div', class_='description__text').text.strip()
                        
                        jobs.append({
                            'title': title,
                            'company': company,
                            'location': location,
                            'description': description,
                            'application_link': link
                        })
                        
                        # Polite delay between requests
                        time.sleep(randint(2, 5))
                        
                    except Exception as e:
                        self.logger.error(f"Error scraping job: {e}")
                        continue
                
                # Add randomized delay between requests
                time.sleep(randint(3, 7))
                page += 1
                
            except Exception as e:
                self.logger.error(f"Error scraping page {page}: {e}")
                break
                
        return jobs
