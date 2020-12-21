
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

driver.implicitly_wait(1)

jobsearchbar = driver.find_element_by_id('1484')
jobsearchbar.send_keys('data science')

submitbutton = driver.find_element_by_id('1488-submit')
submitbutton.click()

pagenumber = 1

skilldict = {}

while True:

	driver.implicitly_wait(1)

	joblinkpage = driver.find_elements_by_class_name('link')

	for x in range(18,len(joblinkpage)):

		joblinkpage = driver.find_elements_by_class_name('link')

		driver.implicitly_wait(1)
		
		try:	

			# WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="WSJTheme--day-link--19pByDpZ "][@href]')))

			print(x,'/ 20 Accessing the following link:', joblinkpage[x].get_attribute('href'))

			#scraping the job link
			job_link = joblinkpage[x].get_attribute('href')
			print('Job Link is', job_link)

			joblinkpage[x].click()


			#scraping each individual posting 

			

			#scraping the job title 
			try:
				
				job_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//h2[@class='banner__title banner__title--details']"))).text
				print('Job Title text is',job_title)
				
			except:
				job_title = ''
				print('Failed to get Job title')
				pass

			#scraping the location
			try:
				#<div class="banner__subtitle">
				location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='banner__subtitle']"))).text
				print('Location text is',location)
			except:
				location = ''
				print('Failed to get Location')
				pass

			#scraping the job number ID
			try:
				job_loc_and_ID = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//div[@class='left']//p")))
				job_loc = job_loc_and_ID[0].text
				job_ID = job_loc_and_ID[1].text
				print('Job ID is',job_ID)
				print('Job Loc is', job_loc)
				
			except:
				job_loc = ''
				job_ID = ''
				print('Failed to get Job ID')
				print('Failed to get Job Loc')
				pass

			#scraping the job details 
			try:
				
				driver.implicitly_wait(1)

				posting_text = ''
				text = driver.find_elements_by_xpath(".//div[@class='article__content article__content--rich-text']")
				for ele in text:
					posting_text += ele.text
				print('Posting Text is',posting_text)
			except (NoSuchElementException, StaleElementReferenceException) as e:
				posting_text = ''
				pass

			try:
				# index_YouHave = posting_text.index('You Have:')
				index_YouHave = re.search(r"Basic Qualifications:|You Have:",string1).start()
				index_NiceIfYouHave = re.search(r"Additional Qualifications:|Nice If You Have:",string1).start()
				# for m in re.finditer('of experience with', text):
				# 	if (m.start() > index_YouHave) and (m.start() < index_NiceIfYouHave):

				#CREATE REGEX MATCHING FORMULA THAT WILL MAP YEARS OF EXPERIENCE TO CORRESPONDING DESIRED SKILLS 

			except:
				pass


			print('Scraped position')
			driver.back()
		except:
			print('Position Scraping Failed')
			continue
	try:
		nextbutton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Next')))
		
		print(nextbutton)
		print(nextbutton.get_attribute('href'))
		
		driver.get(nextbutton.get_attribute('href'))

		pagenumber += 1

		print('Success: Accessed Page #', pagenumber)
	except:
		print('Accessed all pages')
		break

