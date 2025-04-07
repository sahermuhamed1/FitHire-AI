from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GlassdoorScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def scrape_jobs(self, keywords, location, num_jobs=10):
        jobs = []
        base_url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={keywords}&locT=N&locId={location}"
        
        try:
            self.driver.get(base_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-search-card"))
            )
            
            job_cards = self.driver.find_elements(By.CLASS_NAME, "job-search-card")[:num_jobs]
            
            for card in job_cards:
                try:
                    title = card.find_element(By.CLASS_NAME, "job-title").text
                    company = card.find_element(By.CLASS_NAME, "employer-name").text
                    link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
                    
                    if not all([title, company, link]):
                        continue
                        
                    job = {
                        'title': title,
                        'company': company,
                        'location': card.find_element(By.CLASS_NAME, "location").text,
                        'description': self._get_description(link),
                        'application_link': link,
                        'posted_date': datetime.now().strftime('%Y-%m-%d'),
                        'source': 'glassdoor'
                    }
                    jobs.append(job)
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error processing Glassdoor job: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping Glassdoor: {e}")
        finally:
            self.driver.quit()
            
        return jobs
        
    def _get_description(self, url):
        try:
            self.driver.get(url)
            description = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobDescriptionContent"))
            )
            return description.text
        except:
            return ""
