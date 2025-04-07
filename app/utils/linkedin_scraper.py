from bs4 import BeautifulSoup
from datetime import datetime
import requests
from time import sleep
from .base_scraper import BaseScraper

class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        
    def scrape_jobs(self, keywords, location, num_jobs=10):
        jobs = []
        offset = 0
        limit = min(num_jobs, 25)  # LinkedIn's max per page is 25
        
        try:
            while len(jobs) < num_jobs:
                params = {
                    'keywords': keywords,
                    'location': location,
                    'pageSize': limit,
                    'start': offset,
                    'sortBy': 'R'  # Sort by relevance
                }
                
                response = self.make_request(self.base_url, params)
                if not response or response.status_code != 200:
                    break
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', {'class': 'job-search-card'})
                
                if not job_cards:
                    break
                
                for card in job_cards:
                    if len(jobs) >= num_jobs:
                        break
                        
                    try:
                        job = self._parse_job_card(card)
                        if job:
                            jobs.append(job)
                    except Exception as e:
                        print(f"Error parsing job card: {e}")
                        continue
                    
                    # Respect rate limits
                    sleep(1)
                
                offset += len(job_cards)
                if len(job_cards) < limit:
                    break
                    
        except Exception as e:
            print(f"Error in LinkedIn scraping: {e}")
            
        return jobs
    
    def _parse_job_card(self, card):
        """Extract job information from a job card"""
        try:
            title_elem = card.find('h3', {'class': 'base-search-card__title'})
            company_elem = card.find('h4', {'class': 'base-search-card__subtitle'})
            link_elem = card.find('a', {'class': 'base-card__full-link'})
            
            if not all([title_elem, company_elem, link_elem]):
                return None
                
            job_url = link_elem['href']
            
            return {
                'title': title_elem.text.strip(),
                'company': company_elem.text.strip(),
                'location': card.find('span', {'class': 'job-search-card__location'}).text.strip(),
                'description': self._get_job_description(job_url),
                'application_link': job_url,
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'linkedin'
            }
        except Exception as e:
            print(f"Error parsing job elements: {e}")
            return None
            
    def _get_job_description(self, url):
        """Get the full job description"""
        try:
            response = self.make_request(url)
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                desc_elem = soup.find('div', {'class': 'show-more-less-html__markup'})
                return desc_elem.text.strip() if desc_elem else ''
        except Exception as e:
            print(f"Error getting job description: {e}")
        return ''
