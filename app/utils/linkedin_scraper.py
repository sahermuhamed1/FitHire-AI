from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .base_scraper import BaseScraper
import time

class LinkedInScraper(BaseScraper):
    def scrape_jobs(self, keywords, location, num_jobs=10):
        jobs = []
        base_url = "https://www.linkedin.com/jobs/search"
        
        try:
            params = {
                'keywords': keywords,
                'location': location,
                'sortBy': 'DD',
                'f_TPR': 'r2592000'  # Last 30 days
            }
            
            response = self.make_request(base_url, params)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job_cards = soup.find_all('div', {'class': 'job-search-card'})[:num_jobs]
            
            for card in job_cards:
                try:
                    link = card.find('a', {'class': 'job-search-card__link'})
                    if not link:
                        continue
                        
                    job = {
                        'title': card.find('h3', {'class': 'job-search-card__title'}).get_text(strip=True),
                        'company': card.find('h4', {'class': 'job-search-card__company-name'}).get_text(strip=True),
                        'location': card.find('span', {'class': 'job-search-card__location'}).get_text(strip=True),
                        'description': self._get_job_description(link['href']),
                        'application_link': link['href'],
                        'source': 'linkedin',
                        'posted_date': datetime.now().strftime('%Y-%m-%d')
                    }
                    
                    if all(job.values()):
                        jobs.append(job)
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error processing LinkedIn job: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
            
        return jobs
    
    def _get_job_description(self, url):
        try:
            response = self.make_request(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            desc = soup.find('div', class_='show-more-less-html__markup')
            return desc.get_text(strip=True) if desc else ''
        except:
            return ''
            
    def _parse_date(self, time_element):
        if not time_element:
            return datetime.now().strftime('%Y-%m-%d')
        # Parse LinkedIn date format
        return datetime.strptime(time_element['datetime'], '%Y-%m-%d').strftime('%Y-%m-%d')
