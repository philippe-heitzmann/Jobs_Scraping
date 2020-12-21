
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
from collections import defaultdict


#input Booz Allen job postings url 
#output .json file 

#defining function used to match years of experience to desired skills 

def sequen_zip(lst, n):
    newlist = list(zip(*(lst[i:] for i in range(n))))
    newlist.append(tuple([tuple(lst[-1]),tuple(['0',-1])]))
    return newlist

#regex patter match for years of experience formatting
p = re.compile(r'[0-9]+\+')


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

results_dict = {}
skill_dict = {}

while True:

	driver.implicitly_wait(1)

	joblinkpage = driver.find_elements_by_class_name('link')

	for x in range(len(joblinkpage)):

		joblinkpage = driver.find_elements_by_class_name('link')

		driver.implicitly_wait(1)


		match_list_basic = []

		match_list_plus = []

		exp_dict_basic = defaultdict(list)

		exp_dict_plus = defaultdict(list)
		
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
				# print('Posting Text is',posting_text)
			except (NoSuchElementException, StaleElementReferenceException) as e:
				posting_text = ''
				pass

			try:
				# index_YouHave = posting_text.index('You Have:')
				index_YouHave = re.search(r"Basic Qualifications:|You Have:",posting_text).start()
				index_NiceIfYouHave = re.search(r"Additional Qualifications:|Nice If You Have:",posting_text).start()

				print('Index you have is:', index_YouHave)
				
				print('Index nice if you have is:', index_NiceIfYouHave)

				posting_text_you_have = posting_text[index_YouHave:index_NiceIfYouHave]
				posting_text_nice_if_you_have = posting_text[index_NiceIfYouHave:]

				print("Posting text you have is:", posting_text_you_have)

				print("Posting text nice if you have is:", posting_text_nice_if_you_have)

				 
				basic_dict = defaultdict(list)
				pref_dict = defaultdict(list)

				for m in p.finditer(posting_text_you_have):
					basic_dict[m.group()].append(posting_text_you_have[m.start():posting_text_you_have[m.start():].index('\n')])

				for m in p.finditer(posting_text_nice_if_you_have):
					pref_dict[m.group()].append(posting_text_nice_if_you_have[m.start():posting_text_nice_if_you_have[m.start():].index('\n')])
				

				# for m in p.finditer(posting_text_nice_if_you_have):
				# 	match_list_plus.append(tuple([m.group(),m.start()]))


				# if len(match_list_basic) > 0:
				# 	for g in sequen_zip(match_list_basic, 2):
				# 		exp_dict_basic[g[0][0][0]].append(posting_text_you_have[g[0][1]:g[1][1]])
				# else:
				# 	pass
				
				# if len(match_list_plus) > 0:
				# 	for g in sequen_zip(match_list_plus, 2):
				# 		exp_dict_plus[g[0][0][0]].append(posting_text_nice_if_you_have[g[0][1]:g[1][1]])
				# else:
				# 	pass


			except:
				print('Experience Scraping Failed')
				pass


			try:
				results_dict['job_title'] = job_title
				results_dict['location'] = location
				results_dict['job_ID'] = job_ID
				results_dict['job_link'] = job_link
				# results_dict['basic_qual'] = dict(exp_dict_basic)
				# results_dict['preferred_qual'] = dict(exp_dict_plus)
				results_dict['basic_qual'] = dict(basic_dict)
				results_dict['preferred_qual'] = dict(pref_dict)
				
				key1 = job_title + ' ' + job_ID

				skill_dict[key1] = results_dict

				print(skill_dict)

			except:
				print('Error adding to skill_dict')

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

