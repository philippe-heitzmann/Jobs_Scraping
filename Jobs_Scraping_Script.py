
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os 
from bs4 import BeautifulSoup 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains


url = "https://www.amazon.jobs/en/"


chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(), 	options=chrome_options)

driver.get(url)


driver.implicitly_wait(5)
# jobsearchbar = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'search_typeahead')))
# jobsearchbar = driver.find_element_by_id('search_typeahead')
print(jobsearchbar)
jobsearchbar.click()
# driver.execute_script("document.getElementById('search_typeahead').setAttribute('value', 'data science')")
# jobsearchbar.click()
# jobsearchbar.send_keys("data science")
# 
# driver.execute_script("document.getElementsById('search-typeahead')[0].value='password'")

search_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'search-button')))
search_button.click()