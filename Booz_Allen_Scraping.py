
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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

#input Booz Allen job postings url 
#output .json file 

url = "https://careers.boozallen.com/jobs/search"


chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(), 	options=chrome_options)

driver.get(url)

jobsearchbar = driver.find_element_by_id('1484')
jobsearchbar.send_keys('data science')

submitbutton = driver.find_element_by_id('1488-submit')
submitbutton.click()

while True:

	driver.implicitly_wait(1)

	joblinkpage = driver.find_elements_by_class_name('link')

	for x in range(18,len(joblinkpage)):

		joblinkpage = driver.find_elements_by_class_name('link')

		driver.implicitly_wait(1)
		
		try:	

			# WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="WSJTheme--day-link--19pByDpZ "][@href]')))

			print(x,'/ 20 Accessing the following link:', joblinkpage[x].get_attribute('href'))
			joblinkpage[x].click()
			#scraping each individual posting 

			#this is a Github test

			print('Scraped position')
			driver.back()
		except:
			print('Position Scraping Failed')
			continue
	try:
		driver.implicitly_wait(5)

		# nextbutton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Next >>')))

		nextbutton = driver.find_element_by_link_text('Next >>')
		nextbutton.click()
		print('Success: Accessed Next Page')
	except:
		print('Failed: Did not access next page')
		break

