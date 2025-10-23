"""
hireitpeople_java_scraper_single_windows.py

Scrapes a single Java Developer resume from HireITPeople.
Requirements:
    pip install selenium pandas beautifulsoup4

Make sure:
1. Chrome is installed on Windows.
2. chromedriver.exe matches your Chrome version and is placed in the same folder as this script.
"""

import time
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import os

# ---------------- CONFIG ----------------
BASE_URL = "https://www.hireitpeople.com/resume-database/64-java-developers-architects-resumes"
OUTPUT_CSV = "java_resume_single.csv"
DELAY = 1.0  # seconds
HEADLESS = True  # True = browser hidden

# ChromeDriver path (same folder as script)
CHROMEDRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")

# ---------------- SETUP SELENIUM ----------------
chrome_options = Options()
if HEADLESS:
    chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--log-level=3")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# ---------------- HELPER FUNCTIONS ----------------
def generate_id(url: str) -> int:
    """Generate a unique numeric ID from the URL."""
    return int(hashlib.md5(url.encode("utf-8")).hexdigest(), 16)

def get_resume_links_from_page(driver) -> list:
    """Get all resume links on the current page."""
    links = []
    anchor_elements = driver.find_elements(By.CSS_SELECTOR, "a")
    for a in anchor_elements:
        href = a.get_attribute("href")
        if href and "/resume-database/64-java-developers-architects-resumes/" in href and href.endswith("-2"):
            links.append(href)
    return list(set(links))

def extract_resume(driver, url: str) -> dict:
    """Extract raw HTML and text of a resume."""
    data = {"url": url, "category": "java-developers", "raw_html": "", "text": ""}
    driver.get(url)
    time.sleep(DELAY)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    div = soup.find("div", {"id": "document"})
    if div:
        data["raw_html"] = str(div)
        data["text"] = div.get_text(separator="\n", strip=True)
    return data

# ---------------- MAIN SCRIPT ----------------
try:
    driver.get(BASE_URL)
    time.sleep(DELAY)

    resume_links = get_resume_links_from_page(driver)

    if resume_links:
        first_link = resume_links[0]
        resume_data = extract_resume(driver, first_link)
        resume_data["id"] = generate_id(first_link)

        # Save to CSV
        df = pd.DataFrame([resume_data])
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"Saved one resume to {OUTPUT_CSV}")
    else:
        print("No resume links found on the page.")

finally:
    driver.quit()
