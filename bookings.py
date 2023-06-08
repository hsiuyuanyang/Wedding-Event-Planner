# File: bookings.py
#
# Author: Ankit Kumar
# AndrewID: ankitkum
#
# This file collects information about the hotels shown on the first page of the search results in tripadvisor
# Imported by app.py
#
import requests
from bs4 import BeautifulSoup
import pandas as pd

LANGUAGE = "en-US,en;q=0.5"

def parse_hotel(code, city, state):
    try:
        url = ('https://www.tripadvisor.in/Hotels-'+code+'-'+city+'_'+state+'-Hotels.html')
        user_agent = ({'User-Agent':
                           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                           AppleWebKit/537.36 (KHTML, like Gecko) \
                           Chrome/90.0.4430.212 Safari/537.36',
                       'Accept-Language': 'en-US, en;q=0.5'})
        def get_page_contents(url):
            page = requests.get(url, headers=user_agent)
            return BeautifulSoup(page.text, 'html.parser')

        soup = get_page_contents(url)

        hotels = []
        for name in soup.findAll('div',{'class':'listing_title'}):
            hotels.append(name.text.strip())
        ratings = []
        for rating in soup.findAll('a',{'class':'ui_bubble_rating'}):
            ratings.append(rating['alt'])
        reviews = []
        for review in soup.findAll('a',{'class':'review_count'}):
            reviews.append(review.text.strip())
        prices = []
        for p in soup.findAll('div',{'class':'price-wrap'}):
            prices.append(p.text.replace('₹','').strip())

        hotel_dict = {'Hotel Names': hotels, 'Ratings': ratings, 'Number of Reviews': reviews, 'Prices': prices}
        Hotel_data_frame = pd.DataFrame.from_dict(hotel_dict)
        #Hotel_data_frame.head(10) 
        #Hotel_data_frame.clear()
        row = Hotel_data_frame.shape[0]
        if row != 0:
            print_bad = True
            while print_bad:
                print_input = input("Would you like to print the hotel information? (y/n)")
                if print_input == "y":
                    print(Hotel_data_frame)
                    print_bad = False
                elif print_input == "n":
                    print_bad = False
                else:
                    print("Invalid input.")

            export_bad = True
            while export_bad:
                export_input = input("Would you like to export the hotel information to an Excel file? (y/n)")
                if export_input == "y":
                    Hotel_data_frame.to_excel(state + '_' + city + '_' + "hotels.xlsx")
                    print("Hotel information exported to the current path.")
                    export_bad = False
                elif export_input == "n":
                    export_bad = False
                else:
                    print("Invalid input.")
        else:
            print("Hotel information is not available for now")

    except:
        print("Hotel information is not available for now")
    #Hotel_data_frame.to_excel("hotelssss.xlsx")

if __name__ == '__main__':
    code = "g53449"
    city = "Pittsburgh"
    state = "Pennsylvania"
    parse_hotel(code, city, state)