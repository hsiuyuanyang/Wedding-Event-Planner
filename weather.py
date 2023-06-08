# File: weather.py
# 
# Author: Jahnvi Gupta 
# AndrewID: jahnvig
#
# Given date and location, this file collects weather forcast information on weathertab.com
# Imported by app.py
from bs4 import BeautifulSoup
import requests
import pandas as pd

def geturl(date, year, month, state, city):
    try:
        URL = "https://www.weathertab.com/en/d/" + year + "/" + month + "/united-states/" + state + "/" + city + "/"
        #print(URL)
        file = requests.get(URL)
        soup = BeautifulSoup(file.content, "html.parser")
        daily = soup.find_all("tr", "fct_day")
        getWeatherData(daily,date)
    except:
        print("No Data for Weather Forcast")

def getWeatherData(daily, date):
    dates_len = len(daily)
    dates_list = range(0, dates_len)
    date = date - 1
    df = pd.DataFrame()
    try:
        temp = pd.DataFrame(
            {
                'date': daily[date]['data-dayurl'][48:58],
                'Chances_of_Rain': daily[date].find_all("div", class_=False)[0].get_text(),
                'day': daily[date].find_all("div", class_="text-center text-color fct-day-of-week")[0].get_text(),
                'High Temp': daily[date].find_all("span", class_="label label-danger")[0].get_text(),
                'Low Temp': daily[date].find_all("span", class_="label label-primary")[0].get_text()
            },
            index=[0]
        )
    except:
        temp = pd.DataFrame()
    df = pd.concat([df, temp])
    getDataFrame(df)

def getDataFrame(df):

    df = df.drop_duplicates()
    df.set_index('date', inplace = True)
    #df.to_csv('outputWeather.csv', encoding='utf-8')
    #df.to_excel("output.xlsx")
    print(df)  # final output for the city


if __name__ == '__main__':
    date = 12
    year = '2023'
    month = '05'
    state = 'pennsylvania'
    city = 'pittsburgh'
    geturl(date, year, month, state, city)



