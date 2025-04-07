import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

class GlassdoorScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def scrape_jobs(self, keywords, location, num_jobs=10):
        jobs = []
        base_url = "https://www.glassdoor.com/Job/jobs.htm"
        
        try:
            params = {
                'sc.keyword': keywords,
                'locT': 'C',
                'locId': location,
                'sort.type': 'DATE_DESC'
            }
            
            response = requests.get(base_url, params=params, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job_listings = soup.find_all('li', class_='react-job-listing')[:num_jobs]
            
            for listing in job_listings:
                try:
                    link_element = listing.find('a', class_='jobLink')
                    if not link_element or not link_element.get('href'):
                        continue

                    application_link = 'https://www.glassdoor.com' + link_element['href']
                    
                    # Only create job if all required fields are present
                    title = listing.find('a', class_='jobLink').get_text(strip=True)
                    company = listing.find('div', class_='employer-name').get_text(strip=True)
                    description = listing.find('div', class_='jobDescriptionContent').get_text(strip=True)
                    
                    if not all([title, company, description, application_link]):
                        continue

                    job = {
                        'title': title,
                        'company': company,
                        'location': listing.find('span', class_='loc').get_text(strip=True),
                        'description': description,
                        'application_link': application_link,
                        'posted_date': datetime.now().strftime('%Y-%m-%d'),
                        'source': 'glassdoor'
                    }
                    jobs.append(job)
                    time.sleep(1)
                except Exception as e:
                    print(f"Error processing job listing: {e}")
                    continue
                
        except Exception as e:
            print(f"Error scraping Glassdoor: {e}")
            
        return jobs
