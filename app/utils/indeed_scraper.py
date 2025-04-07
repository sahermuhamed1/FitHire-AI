from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class IndeedScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def scrape_jobs(self, keywords, location, num_jobs=10):
        jobs = []
        base_url = f"https://www.indeed.com/jobs?q={keywords}&l={location}&sort=date"
        
        try:
            self.driver.get(base_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
            )
            
            # Scroll to load more jobs if needed
            self._scroll_to_load_jobs(num_jobs)
            
            job_cards = self.driver.find_elements(By.CLASS_NAME, "job_seen_beacon")[:num_jobs]
            
            for card in job_cards:
                try:
                    job = self._extract_job_data(card)
                    if job:
                        jobs.append(job)
                        time.sleep(1)  # Prevent rate limiting
                        
                except Exception as e:
                    print(f"Error processing Indeed job: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping Indeed: {e}")
        finally:
            self.driver.quit()
            
        return jobs
    
    def _extract_job_data(self, card):
        """Extract data from a job card"""
        try:
            title_elem = card.find_element(By.CLASS_NAME, "jobTitle")
            company_elem = card.find_element(By.CLASS_NAME, "companyName")
            link_elem = title_elem.find_element(By.TAG_NAME, "a")
            
            title = title_elem.text
            company = company_elem.text
            link = link_elem.get_attribute("href")
            
            if not all([title, company, link]):
                return None
                
            return {
                'title': title,
                'company': company,
                'location': card.find_element(By.CLASS_NAME, "companyLocation").text,
                'description': self._get_description(link),
                'application_link': link,
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'indeed'
            }
        except NoSuchElementException:
            return None
            
    def _scroll_to_load_jobs(self, target_count):
        """Scroll the page to load more jobs"""
        current_jobs = 0
        max_scrolls = 5
        scrolls = 0
        
        while current_jobs < target_count and scrolls < max_scrolls:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            current_jobs = len(self.driver.find_elements(By.CLASS_NAME, "job_seen_beacon"))
            scrolls += 1
            
    def _get_description(self, url):
        """Get the full job description"""
        try:
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.get(url)
            
            desc = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobDescriptionText"))
            )
            description = desc.text
            
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            return description
        except:
            return ""
