from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IndeedScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def scrape_jobs(self, keywords, location, num_jobs=10):
        jobs = []
        base_url = f"https://www.indeed.com/jobs?q={keywords}&l={location}&sort=date"
        
        try:
            self.driver.get(base_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
            )
            
            job_cards = self.driver.find_elements(By.CLASS_NAME, "job_seen_beacon")[:num_jobs]
            
            for card in job_cards:
                try:
                    title = card.find_element(By.CLASS_NAME, "jobTitle").text
                    company = card.find_element(By.CLASS_NAME, "companyName").text
                    link = card.find_element(By.CLASS_NAME, "jcs-JobTitle").get_attribute("href")
                    
                    if not all([title, company, link]):
                        continue
                        
                    job = {
                        'title': title,
                        'company': company,
                        'location': card.find_element(By.CLASS_NAME, "companyLocation").text,
                        'description': self._get_description(link),
                        'application_link': link,
                        'posted_date': datetime.now().strftime('%Y-%m-%d'),
                        'source': 'indeed'
                    }
                    jobs.append(job)
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error processing Indeed job: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping Indeed: {e}")
        finally:
            self.driver.quit()
            
        return jobs
        
    def _get_description(self, url):
        try:
            self.driver.get(url)
            description = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobDescriptionText"))
            )
            return description.text
        except:
            return ""
