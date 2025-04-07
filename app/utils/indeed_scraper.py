import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

class IndeedScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def scrape_jobs(self, keywords, location, num_jobs=10):
        jobs = []
        base_url = "https://www.indeed.com/jobs"
        
        try:
            params = {
                'q': keywords,
                'l': location,
                'sort': 'date'
            }
            
            response = requests.get(base_url, params=params, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job_cards = soup.find_all('div', class_='job_seen_beacon')[:num_jobs]
            
            for card in job_cards:
                job = {
                    'title': card.find('h2', class_='jobTitle').get_text(strip=True),
                    'company': card.find('span', class_='companyName').get_text(strip=True),
                    'location': card.find('div', class_='companyLocation').get_text(strip=True),
                    'description': card.find('div', class_='job-snippet').get_text(strip=True),
                    'application_link': 'https://www.indeed.com' + card.find('a')['href'],
                    'posted_date': datetime.now().strftime('%Y-%m-%d')  # Indeed shows relative dates, using current date
                }
                jobs.append(job)
                time.sleep(1)  # Respect rate limits
                
        except Exception as e:
            print(f"Error scraping Indeed: {e}")
            
        return jobs
