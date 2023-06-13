# File: venue.py
#
# Author: Fuman Annie Xie
# AndrewID: fumanx
# 
# This file collects information about venues listed in every page of the search results on weddingwire.com
#
# Imported by app.py
# Imports global_variables.py
#
# while (next_outer_page) {
#	 update page_url
#    create a page_bs object
#    collect links
#    for i in links:
#        parseInnerPage(i)
# }
#
from urllib.request import urlopen
from bs4 import BeautifulSoup
from global_variables import location
import numpy as np
import pandas as pd
#import time
import matplotlib.pyplot as plt

#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import NoSuchElementException

def find_venue_rating(page_bs, new_venue_info_row):
	try:
		rating_value = page_bs.find('span', class_ = 'srOnly').get_text()
		rating_value = rating_value.partition(' ')[0]
		new_venue_info_row.append(float(rating_value))
	except:
		new_venue_info_row.append(np.nan)

def find_number_of_raters(page_bs, new_venue_info_row):
	try:
		number_of_raters = page_bs.find('span', class_ = 'storefrontHeading__reviewsValue').get_text()
		new_venue_info_row.append(int(number_of_raters))
	except:
		new_venue_info_row.append(np.nan)

def find_venue_website(page_bs, new_venue_info_row):
	try:
		website_url = str(page_bs.find('span', class_ = 'link storefrontHeading__contactItem app-storefront-visit-website'))
		start = website_url.find('http')
		website_url = website_url[start: ].replace('&amp;', '&').partition('"')[0]
		new_venue_info_row.append(website_url)
	except:
		new_venue_info_row.append('NA')

def update_bool_type(ans, targets, new_venue_info_row):
	month_set = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 
		         'August', 'September', 'October', 'November', 'December')
	for target in targets:
		if ans.find(target) != -1:
			new_venue_info_row.append('peak' if target in month_set else 'yes')
		else:
			new_venue_info_row.append('off-peak' if target in month_set else 'no')

def find_answer_to_faq(page_bs, new_venue_info_row):
	try:
		faq_list = page_bs.find_all('h3', class_ = "storefrontFaqs__itemTitle")
		ans_list = page_bs.find_all('div', class_ = "storefrontFaqs__itemContent")
		faq_ans_dict = {}
		for i in range(0,len(ans_list)):
			faq = faq_list[i].get_text().strip()
			ans = ans_list[i].get_text().strip()
			try:
				faq_ans_dict[faq] = int(ans.lstrip('$').replace(',', '').split('.')[0])
			except:
				faq_ans_dict[faq] = ans
		
		#update venue max capacity
		new_venue_info_row.append(faq_ans_dict.get("What is the maximum capacity of your venue?", np.nan))
		
		#update venue indoor/outdoor setting
		setting = faq_ans_dict.get("What kind of settings are available?" , None)
		if setting == None:
			na_list = ['NA'] * 3
			new_venue_info_row.extend(na_list)
		else:
			setting_list = ['Indoor', 'Covered Outdoor', 'Uncovered Outdoor']
			update_bool_type(setting, setting_list, new_venue_info_row)
		
		#update site fee
		new_venue_info_row.append(faq_ans_dict.get("What is the starting site fee for wedding receptions during peak season?", np.nan))
		new_venue_info_row.append(faq_ans_dict.get("What is the starting site fee for wedding receptions during off-peak season?", np.nan))
		new_venue_info_row.append(faq_ans_dict.get("What is the starting site fee for wedding ceremonies during peak season?", np.nan))
		new_venue_info_row.append(faq_ans_dict.get("What is the starting site fee for wedding ceremonies during off-peak season?", np.nan))
		
		#update peak/off-peak season
		peak_season = faq_ans_dict.get("What months are included in your peak season?", None)
		if peak_season == None:
			na_list = ['NA'] * 12
			new_venue_info_row.extend(na_list)
		else:
			month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
			              'August', 'September', 'October', 'November', 'December']
			update_bool_type(peak_season, month_list, new_venue_info_row)
	except:
		na_list = ['NA'] * 20
		new_venue_info_row.extend(na_list)

def parse_inner_page(df, page_url):

	html = urlopen(page_url)
	page_bs = BeautifulSoup(html.read(), "lxml") 

	venue_name = page_bs.find('title').get_text()
	venue_name = venue_name.replace('&amp;', '&')
	venue_name = venue_name.partition('-')[0].rstrip()
	#make sure there are no duplicate venues
	if venue_name not in set(df['Venue Name']):
		#store the information in a list
		new_venue_info_row = []
		new_venue_info_row.append(venue_name)
		find_venue_rating(page_bs, new_venue_info_row)
		find_number_of_raters(page_bs, new_venue_info_row)
		find_answer_to_faq(page_bs, new_venue_info_row)
		find_venue_website(page_bs, new_venue_info_row)
		#add the list to the dataframe as a row
		df.loc[len(df.index)] = new_venue_info_row

def parse_outer_page(df, state_id, region_id):
	if state_id != '411':
		outer_page_url = 'https://www.weddingwire.com/shared/search?group_id=1&state_id=' + state_id + '&region_id=' + region_id
	else:
		outer_page_url = 'https://www.weddingwire.com/shared/search?group_id=1&state_id=' + state_id + '&region_id=10084&geozone_id=' + region_id 
	html = urlopen(outer_page_url)
	page_bs = BeautifulSoup(html.read(), "lxml")
	page_numbers = page_bs.find_all('button', class_ = 'pagination__itemButton button button--block button--tertiary app-pagination-link')
	try:
		max_page_number = int(page_numbers[len(page_numbers) - 1].get_text())
	except:
		max_page_number = 1
	#print(max_page_number)
	page_number = 1
	print("Collecting venue information...")
	print("This could take around " + str(max_page_number * 30) + " seconds")
	print("Scraping 1/" + str(max_page_number) + " page(s)")
	while outer_page_url != None:
		try: 
			html = urlopen(outer_page_url)
		except:
			outer_page_url = None
			pass

		page_bs = BeautifulSoup(html.read(), "lxml")

		#collect links to the venue information
		vendor_list = page_bs.find_all('a', class_ = 'vendorTile__title app-vendor-tile-link')

		for i in vendor_list:
			#test
			#if len(venue_info_df.index) == 5:
			#	break
			parse_inner_page(df, i['href'])

		#move to the next page if possible
		page_number += 1
		if page_number <= max_page_number:
			if state_id != '411':
				next_page = 'https://www.weddingwire.com/shared/search?group_id=1&region_id=' + region_id + '&state_id=' + state_id + '&page=' + str(page_number)
			else:
				next_page = 'https://www.weddingwire.com/shared/search?geozone_id=' + region_id + 'group_id=1&region_id=10084&state_id=' + state_id + '&page=' + str(page_number)
			print("Scraping " + str(page_number) + "/" + str(max_page_number) + " page(s)")
		else:
			next_page = None
		
		outer_page_url = next_page

def plot_venue_info(df_with_nan):
	#plot venue information
	print("Here are 5 figures about venues.")
	df = df_with_nan.dropna(axis = 0, how = 'any')

	plot_2_y_axis(df, 'Venue Name', 'Rating', 'Number of Raters')
	plot_2_y_axis(df, 'Venue Name', 'Rating', 'Capacity')
	plot_2_y_axis(df, 'Venue Name', 'Rating', 'Wedding Reception Peak Season Starting Fee($)')

	df_setting = df.loc[ : , 'Indoor': 'Uncovered Outdoor']
	row, col = df_setting.shape
	for i in range(row):
		for j in range(col):
			if df_setting.iloc[i, j] == 'yes':
				df_setting.iloc[i, j] = 1
			else:
				df_setting.iloc[i, j] = 0
	plt.bar(df_setting.columns, df_setting.sum())
	plt.title('Setting')
	plt.show()

	df_season = df.loc[ : , 'Jan': 'Dec']
	row, col = df_season.shape
	for i in range(row):
		for j in range(col):
			if df_season.iloc[i, j] == 'peak':
				df_season.iloc[i, j] = 1
			else:
				df_season.iloc[i, j] = 0
	plt.bar(df_season.columns, df_season.sum())
	plt.title('Peak Season')
	plt.show()

def plot_2_y_axis(df, x_label, y1_label, y2_label):
	#plot a figure with two y axis
	X = np.array(df[x_label])

	Y1 = np.array(df[y1_label])
	Y2 = np.array(df[y2_label])
	fig, ax1 = plt.subplots(figsize =(15, 7))

	ax1.set_xlabel(x_label)
	ax1.tick_params(axis = 'x', labelrotation = 270, labelsize = 7)
	ax1.set_ylabel(y1_label, color = 'red')
	ax1.plot(X, Y1, color = 'red')

	ax2 = ax1.twinx()
	ax2.set_ylabel(y2_label, color = 'blue')
	ax2.scatter(X, Y2, color = 'blue')

	plt.title('Venue Information')
	plt.show()

def parse_venue(df, state_id, region_id, input_state, input_city_id):
	live_bad = True
	while live_bad:
		print("Would you like to scrape venue information now? This could take 1-3 minutes.")
		live_input = input("If you choose no, we are going to use the venue information in Pittsburgh that we have scraped in advance. (y/n)")

		if live_input == "y":
			live_bad = False
			parse_outer_page(df, state_id, region_id)
			
		elif live_input == "n":
			live_bad = False
			df = pd.read_csv('pittsburgh_venue_info.csv', index_col = 0)
			input_state = 'Pennsylvania'
			input_city_id = 3
		else:
			print("Invalid input.")
	print_venue_info(df, input_state, input_city_id)

def print_venue_info(venue_info_df, input_state, input_city_id):
	print(str(len(venue_info_df.index)) + " venues are found!")

	print_bad = True
	while print_bad:
		print_input = input("Would you like to print and plot the venue information? (y/n)")
		if print_input == "y":
			venue_info_df = venue_info_df.sort_values(by = ['Rating'], ascending = False, na_position = 'last')
			print(venue_info_df)
			plot_venue_info(venue_info_df)
			print_bad = False
		elif print_input == "n":
			print_bad = False
		else:
			print("Invalid input.")

	export_bad = True
	while export_bad:
		export_input = input("Would you like to export the venue information to an Excel file? (y/n)")
		if export_input == "y":
			venue_info_df.to_excel(input_state + '_' + location[input_state][(input_city_id - 1) * 3] + '_' + 'venue_info.xlsx')
			print("Venue information exported to the current path.")
			export_bad = False
		elif export_input == "n":
			export_bad = False
		else:
			print("Invalid input.")
			
if __name__ == '__main__':
	#test Pittsburgh
	#print(venue_info_df)
	state_id = "438"
	region_id = "10012"

	#time_start = time.time()
	venue_info = {
				'Venue Name':[], 
				'Rating':[], 
				'Number of Raters':[], 
				'Capacity':[], 
				'Indoor':[], 
				'Covered Outdoor':[], 
				'Uncovered Outdoor':[],
				'Wedding Reception Peak Season Starting Fee($)':[], 
				'Wedding Reception Off-Peak Season Starting Fee($)':[], 
				'Wedding Ceremony Peak Season Starting Fee($)':[], 
				'Wedding Ceremony Off-Peak Season Starting Fee($)':[], 
				'Jan':[] ,'Feb':[] ,'Mar':[] ,'Apr':[] ,'May':[] ,'Jun':[] ,
				'Jul':[] ,'Aug':[] ,'Sept':[] ,'Oct':[] ,'Nov':[] ,'Dec':[] ,
				'Website': []
			}

	venue_info_df = pd.DataFrame(venue_info)
	parse_venue(venue_info_df, state_id, region_id, 'Pennsylvania', 3)
	venue_info_df.to_csv('pittsburgh_venue_info.csv')
	#time_end = time.time()
	#time_c= time_end - time_start 
	#print('time cost', time_c, 's')
























