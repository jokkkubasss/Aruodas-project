from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
import pandas as pd
#from test import return_link, return_element_text, return_area, return_room_n, return_floor_n, return_floor_total, return_year, return_building_type, return_heating_type, return_equipment_state

import time

urls_private = []
urls_company = []

def prepare_url(owner, page):
	url_prepared = 'https://www.aruodas.lt/butai/vilniuje/puslapis/'+ str(page) +'/?FOwnerDbId' + str(owner) + '=1'
	return url_prepared

def return_link(row_n):
	try:
		element = driver.find_element_by_css_selector('body > div.main.filter-form > div.content > div.main-content > table > tbody > tr:nth-child(' +  str(row_n) + ') > td.list-adress > h3 > a')
		url_link = element.get_attribute('href')
	except NoSuchElementException:
		url_link = ''
	return url_link

def return_element_text(css_selector):
	try:
		element = driver.find_element_by_css_selector(css_selector).text
	except:
		element = ''
	return element

def return_title():
	try:
		element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[1]/div[4]/h1").text
	except:
		element = ''
	return element

def return_area():
	try:
		element = driver.find_element_by_xpath("//*[contains(text(), 'Plotas:')]/following-sibling::dd").text
	except:
		element = ''
	return element

def return_room_n():
	try:
		element = driver.find_element_by_xpath("//*[contains(text(), 'Kambarių sk.:')]/following-sibling::dd").text
	except:
		element = ''
	return element

def return_floor_n():
	try:
		element = driver.find_element_by_xpath("//*[contains(text(), 'Aukštas:')]/following-sibling::dd").text
	except:
		element = ''
	return element

def return_floor_total():
	try:
		element = driver.find_element_by_xpath("//*[contains(text(), 'Aukštų sk.:')]/following-sibling::dd").text
	except:
		element = ''
	return element

def return_year():
	try:
		element = driver.find_element_by_xpath("//*[contains(text(), 'Metai:')]/following-sibling::dd").text
	except:
		element = ''
	return element

def return_building_type():
	try:
		element = driver.find_element_by_xpath("//*[contains(text(), 'Pastato tipas:')]/following-sibling::dd").text
	except:
		element = ''
	return element

def return_heating_type():
	try:
		element = driver.find_element_by_xpath("//*[contains(text(), 'Šildymas:')]/following-sibling::dd").text
	except:
		element = ''
	return element

def return_equipment_state():
	try:
		element = driver.find_element_by_xpath("//*[contains(text(), 'Įrengimas:')]/following-sibling::dd").text
	except:
		element = ''
	return element

def return_crime():
	try:
		element = driver.find_element_by_xpath("//div[@class='arrow_line_left']/span[@class='cell-data']").text
	except:
		element = ''
	return element




driver = webdriver.Chrome()


for o in [0, 1]:
	for page in range(1, 93):
		driver.get(prepare_url(o, page))
		time.sleep(2)

		for i in range(3, 34):
			if o == 0:
				urls_private.append(return_link(i))
			else:
				urls_company.append(return_link(i))

dict_links = {'urls_private': urls_private, 'urls_company': urls_company}

df = pd.DataFrame(dict_links)
df.to_csv('C://Users//jkras//Desktop//urls_csv.csv')


dict_links = pd.read_csv('C://Users//jkras//Desktop//urls_company.csv')

scraped_data = {'title': [], 'price': [], 'area': [], 'room_n': [], 'floor_n': [], 'floor_total': [], 'year': [], 'building_type': [], 'heating_type': [], 'equip_state': [], 'nearest_kindergarten': [], 'nearest_school': [], 'nearest_shop': [], 'nearest_station': [], 'crime_last_month': [], 'owner_type': [] }     

for url_type in dict_links:
	for url in dict_links[url_type]:
		time.sleep(2)
		if len(url) > 1:
			try:
				driver.get(url)
			except InvalidArgumentException:
				pass

			scraped_data['title'].append(return_title())
			scraped_data['price'].append(return_element_text('body > div.main > div.content > div.main-content > div.obj-cont > div.price-block > div > span.price-eur'))
			scraped_data['area'].append(return_area())
			scraped_data['room_n'].append(return_room_n())
			scraped_data['floor_n'].append(return_floor_n())
			scraped_data['floor_total'].append(return_floor_total())
			scraped_data['year'].append(return_year())
			scraped_data['building_type'].append(return_building_type())
			scraped_data['heating_type'].append(return_heating_type())
			scraped_data['equip_state'].append(return_equipment_state())
			scraped_data['nearest_kindergarten'].append(return_element_text('#advertStatisticHolder > div:nth-child(1) > div.statistic-info-cell-main > span.cell-data'))
			scraped_data['nearest_school'].append(return_element_text('#advertStatisticHolder > div:nth-child(2) > div.statistic-info-cell-main > span.cell-data'))
			scraped_data['nearest_shop'].append(return_element_text('#advertStatisticHolder > div:nth-child(3) > div.statistic-info-cell-main > span.cell-data'))
			scraped_data['nearest_station'].append(return_element_text('#advertStatisticHolder > div:nth-child(4) > div.statistic-info-cell-main > span.cell-data'))
			scraped_data['crime_last_month'].append(return_crime())
			if url_type == 'urls_private':
				scraped_data['owner_type'].append('private')
			else:
				scraped_data['owner_type'].append('company')
	df_data = pd.DataFrame(scraped_data)
	df_data.to_csv('C://Users//jkras//Desktop//scraped_data.csv')

df_data = pd.DataFrame(scraped_data)
df_data.to_csv('C://Users//jkras//Desktop//scraped_data.csv')
print('Done!')

