# File: app.py, main program
#
# Author: Fuman Annie Xie       
# AndrewID: fumanx
#
# This file imports the separate scraping files written by our group members:
# AndrewID: hsiuyuay, fumanx, ankitkum, jahnvig 
# Imports venue.py, bookings.py, my_calendar.py, weather.py, global_variables.py
#
import venue
import bookings
import my_calendar
import weather
from global_variables import *
from datetime import date

def greeting():
	print("Welcome to Plan Your Wedding!")
	print("Our APP will provide you with calendar, weather, venue, and hotel information based on your selected date and location.") 
	print("Please follow the instructions. Thank you!")

def ask_for_location(input_month, input_day):
	state_bad = True
	input_state = ""
	input_city_id = 0
	while state_bad:
		input_state = input("Please input the full name of the state: ").title()
		if input_state in location.keys():
			state_bad = False
		else:
			print("Invalid value.")

	print("Please choose a city ID from the following cities: ")
	for i in range(0, len(location[input_state]), 3):
		print(str((i + 3)//3) + ' ' + location[input_state][i])

	city_bad = True
	while city_bad:
		try:
			input_city_id = int(input("City chosen: "))
			#print(input_city_id)
			if input_city_id in range(1, len(location[input_state])//3 + 1):
				city_bad = False
			else:
				print("Invalid value.")
		except:
			print("Please input a valid number.")

	state_id = str(state[input_state])
	region_id = str(location[input_state][input_city_id * 3 - 2])
	input_city = location[input_state][(input_city_id - 1) * 3]

#weather info
	weather_state = input_state.lower().replace(' ', '-').replace('.', '-')
	weather_city = input_city.lower().replace(' ', '-').replace('.', '-')
	print("Weather forecast information: ")
	weather.geturl(input_day, '2023', '0' + str(input_month) if input_month < 10 else str(input_month), weather_state, weather_city)

#venue info
	venue.parse_venue(venue_info_df, state_id, region_id, input_state, input_city_id)
	
#hotel scraping
	print("Collecting hotel information...")
	code = str(location[input_state][input_city_id * 3 - 1])
	hotel_state = input_state.replace(' ', '_')
	hotel_city = input_city.replace(' ', '_')

	bookings.parse_hotel(code, hotel_city, hotel_state)

def ask_for_date():
	date_bad = True
	while date_bad:
		try:
			input_month = int(input("Choose a date in 2023. \nPlease input the month in numbers(e.g. for Jan, input 1): "))
			input_day = int(input("Please input the day: "))
			try:
				date(2023, input_month, input_day)
				date_bad = False
			except:
				print("Please input a valid date.")
		except:
			print("Please input a valid number.")

	chosen_date = str(date(2023, input_month, input_day))
#date info, table format
	print(calendar_2023_df.loc[chosen_date])
	return input_month, input_day

if __name__ == '__main__':
	greeting()
	calendar_2023_df = my_calendar.init_calendar()

	main_input = True

	while main_input:
		#get date
		input_month = 0
		input_day = 0
		try_another_date = True
		next_date = "y"
		while try_another_date:
			if next_date == "y":
				input_month, input_day = ask_for_date()
			next_date = input("Would you like to try another date? (y/n)")
			if next_date == "y":
				pass
			elif next_date == "n":
				try_another_date = False
			else:
				print("Invalid input.")

		#get location
		look_for_next_city = True
		next_city = "y"
		while look_for_next_city:
			if next_city == "y":
				ask_for_location(input_month, input_day)
			next_city = input("Would you like to look for venues in another city? (y/n)")
			if next_city == "y":
				pass
			elif next_city == "n":
				look_for_next_city = False
			else:
				print("Invalid input.")
		
		#exit the program
		another_trial = True
		trial = 'y'
		while another_trial:
			trial = input("Would you like to quit the program? (y/n)")
			if trial == "y":
				print("Thank you for trying our product! See you again!")
				another_trial = False
				main_input = False
				break
			elif trial == "n":
				break
			else:
				print("Invalid input.")
