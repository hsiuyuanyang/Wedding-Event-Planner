# File: my_calendar.py
#
# Author: Hsiu-yuan Yang
# AndrewID: hsiuyuay
# This file collects calendar and holiday information and 
# ausipicious dates in Lunar and Hindu Calendars from several websites
# 
# Imported by app.py

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def base_calendar(begin_date, end_date):
    calendar_df = pd.DataFrame(
        {
            "Date": pd.date_range(begin_date, end_date),
            "Day": [0] * 365,
            "Lunar Auspicious Date": [0] * 365,
            "Hindu Auspicious Date": [0] * 365,
            "US Holiday": ["N/A"] * 365,
            "Countdown Days": [0] * 365
        }
    )

    calendar_df["Date_Datetime"] = pd.to_datetime(calendar_df["Date"])

    calendar_df["Date"] = calendar_df["Date_Datetime"].dt.strftime("%Y-%m-%d")
    calendar_df["Date"] = calendar_df["Date"].astype(str)
    # print(calendar_df.dtypes)
    # print(calendar_df.Date)
    return calendar_df


def get_day(calendar_df):
    # map the week of days with Monday, Tuesday, ..., Sunday for easier view
    dw_mapping = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    calendar_df["Day"] = calendar_df['Date_Datetime'].dt.weekday.map(dw_mapping)
    return calendar_df


# webscraping for auspicious hindu marriage dates 2023
def hindu_auspicious_dates_2023(calendar_df):
    html = urlopen('https://weddingz.in/blog/wedding-dates-check-out-auspicious-hindu-marriage-dates-for-your-big-day/')
    bsyc = BeautifulSoup(html.read(), "lxml")
    #fout = open('auspicious_temp.txt', 'wt', encoding='utf-8')
    #fout.write(str(bsyc))
    #fout.close()

    # get a list of the figure classes, since the stuff we want is in a table figure
    fig_list = bsyc.findAll('figure')

    # for self-examination
    # print(fig_list)

    # the 1st figure is actually a summary of all suspicious dates, can directly use it
    # for self-examination
    # print(fig_list[0])
    target_fig = fig_list[0]

    # dig out the tds in our target figure
    td_list = target_fig.findAll('td')
    # for self-examination
    # print(td_list)

    # seeing the top 3 tds are not what we want, exclude it first
    td_list2 = td_list[3:]
    # for self-examination
    # print(td_list2)

    # from the data, we see that each month is composed of 3 tds,
    # with the first one as an index (which we might not need),
    # the second one as the month name, and
    # the third one listing out all the auspicious dates in that month

    month_list = []
    date_list = []
    for i in range(len(td_list2)):
        if i % 3 == 1:
            month_list.append(td_list2[i].text)
        elif i % 3 == 2:
            date_list.append(td_list2[i].text)

    # clean up the date values, e.g. from 15th to 15 for each date_list
    updated_date_list = []
    for rec in date_list:
        extract_num = []
        dates = rec.split(",")
        for d in dates:
            extract_num.append(d[:-2])

        updated_date_list.append(extract_num)

    month_date_dict = {}
    for i in range(len(month_list)):
        month_date_dict[month_list[i]] = updated_date_list[i]

    # change the month values to numbers for easier alignment later
    month_to_num = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                    'July': '07', 'August': '08',
                    'September': '09', 'October': '10', 'November': '11', 'December': '12'}
    month_date_dict = dict((month_to_num[key], value) for (key, value) in month_date_dict.items())
    # print(month_date_dict)

    hindu_dates = []
    for k, v in month_date_dict.items():
        str_date_month = '2023-' + k
        for i in v:
            i = i.lstrip()
            if len(i) == 1:
                i = "0" + i
            str_date_full = str_date_month + '-' + i.lstrip('')
            hindu_dates.append(str_date_full)
    # print(hindu_dates)

    for i in range(len(calendar_df)):

        if calendar_df.iloc[i, 0] in hindu_dates:
            calendar_df.iloc[i, 3] = 'Yes'
        else:
            calendar_df.iloc[i, 3] = 'No'

    # print(calendar_df[['Date', 'Hindu Auspicious Date']].head(20))
    return calendar_df


# webscraping for auspicious lunar marriage dates 2023
def lunar_auspicious_dates_2023(calendar_df):
    source = urlopen(
        'https://brides.she.com/guides/%E7%B5%90%E5%A9%9A%E5%A5%BD%E6%97%A5%E5%AD%90-2023-%E9%9B%99%E6%98%A5%E5%85%BC%E9%96%8F%E6%9C%88-%E6%BA%96%E6%96%B0%E4%BA%BA-%E6%93%87%E6%97%A5%E7%A6%81%E5%BF%8C/')
    bsyc = BeautifulSoup(source.read(), "lxml")
    #fout = open('lunar_auspicious_temp.txt', 'wt', encoding='utf-8')
    #fout.close()

    # get a list of the div classes
    div_list = bsyc.findAll('div')
    # for self-examination
    # print(div_list)

    # we can see that there are many div classes, and our target data are stored in the below indexes:
    jan_list = div_list[27:38]
    feb_list = div_list[40:48]
    mar_list = div_list[50:60]
    apr_list = div_list[62:70]
    may_list = div_list[72:83]
    jun_list = div_list[85:96]
    jul_list = div_list[98:113]
    aug_list = div_list[115:126]
    sep_list = div_list[128:138]
    oct_list = div_list[140:152]
    nov_list = div_list[154:161]
    dec_list = div_list[163:169]

    # extract the text from our target divs
    jans = [i.text[:10] for i in jan_list]
    febs = [i.text[:10] for i in feb_list]
    mars = [i.text[:10] for i in mar_list]
    aprs = [i.text[:10] for i in apr_list]
    mays = [i.text[:9] for i in may_list]
    juns = [i.text[:9] for i in jun_list]
    juls = [i.text[:10] for i in jul_list]
    augs = [i.text[:9] for i in aug_list]
    seps = [i.text[:9] for i in sep_list]
    octs = [i.text[:10] for i in oct_list]
    novs = [i.text[:10] for i in nov_list]
    decs = [i.text[:10] for i in dec_list]

    # for self-examination
    # print(jans)
    # print(febs)
    # print(mars)
    # print(aprs)
    # print(mays)
    # print(juns)
    # print(juls)
    # print(augs)
    # print(seps)
    # print(octs)
    # print(novs)
    # print(decs)

    # concatenate to create date strings, tidy up and store into lunar dates list
    lunar_dates = []
    for i in jans:
        if i[-1] != " ":
            element = i[:4] + '-0' + i[5] + '-' + i[7:9]
        else:
            element = i[:4] + '-0' + i[5] + "-0" + i[7]
        lunar_dates.append(element)

    for i in febs:
        if i[-1] != " ":
            element = i[:4] + '-0' + i[5] + '-' + i[7:9]
        else:
            element = i[:4] + '-0' + i[5] + "-0" + i[7]
        lunar_dates.append(element)

    for i in mars:
        if i[-1] != " ":
            element = i[:4] + '-0' + i[5] + '-' + i[7:9]
        else:
            element = i[:4] + '-0' + i[5] + "-0" + i[7]
        lunar_dates.append(element)

    for i in aprs:

        if i[7] == "9":  # special case since the data on the website is not neat
            element = '2023-04-09'
        elif i[-1] != " ":
            element = i[:4] + '-0' + i[5] + '-' + i[7:9]
        else:
            element = i[:4] + '-0' + i[5] + "-0" + i[7]
        lunar_dates.append(element)

    for i in mays:
        if i[-2] == "1" or i[-2] == "2" or i[-2] == "3":
            element = i[:4] + '-0' + i[5] + '-' + i[7:9]
        else:
            element = i[:4] + '-0' + i[5] + "-0" + i[7]
        lunar_dates.append(element)

    for i in juns:
        if i[-2] == "1" or i[-2] == "2" or i[-2:] == "30":
            element = i[:4] + '-0' + i[5] + '-' + i[7:9]
        else:
            element = i[:4] + '-0' + i[5] + "-0" + i[7]
        lunar_dates.append(element)

    for i in juls:
        if i[-1] != " ":
            element = i[:4] + '-0' + i[5] + '-' + i[7:9]
        else:
            element = i[:4] + '-0' + i[5] + "-0" + i[7]
        lunar_dates.append(element)

    for i in augs:
        if i[-2:] == "10" or i[-2:] == "13" or i[-2:] == "14" or i[-2:] == "16" or i[-2:] == "17" or i[-2] == "2":
            element = i[:4] + '-0' + i[5] + '-' + i[7:9]
        else:
            element = i[:4] + '-0' + i[5] + "-0" + i[7]
        lunar_dates.append(element)

    for i in seps:
        if i[-2] == "1" or i[-2] == "2":
            element = i[:4] + '-0' + i[5] + '-' + i[7:9]
        else:
            element = i[:4] + '-0' + i[5] + "-0" + i[7]
        lunar_dates.append(element)

    for i in octs:
        if (i[-2] == "1" and i[-1] in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]) or i[-2] == "2" or i[
                                                                                                             -2:] == "30":
            element = i[:4] + '-' + i[5:7] + '-' + i[8:10]
        else:
            element = i[:4] + '-' + i[5:7] + "-0" + i[8]
        lunar_dates.append(element)

    for i in novs:
        if i[-2] == "1" or i[-2] == "2":
            element = i[:4] + '-' + i[5:7] + '-' + i[8:10]
        else:
            element = i[:4] + '-' + i[5:7] + "-0" + i[8]
        lunar_dates.append(element)

    for i in decs:
        if i[-2] == "1" or (i[-2] == "2" and i[-1] in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]):
            element = i[:4] + '-' + i[5:7] + '-' + i[8:10]
        else:
            element = i[:4] + '-' + i[5:7] + "-0" + i[8]
        lunar_dates.append(element)

    # print(lunar_dates)
    for i in range(len(calendar_df)):

        if calendar_df.iloc[i, 0] in lunar_dates:
            calendar_df.iloc[i, 2] = 'Yes'
        else:

            calendar_df.iloc[i, 2] = 'No'

    # print(calendar_df[['Date', 'Lunar Auspicious Date']].head(20))
    return calendar_df


def get_US_holiday(calendar_df):
    us_holiday = pd.read_excel("us-holidays-2023-list-classic-en-us.xlsx", header=1)
    us_holiday = us_holiday.drop(columns=['Unnamed: 1'])

    # print(us_holiday.head())
    # print(us_holiday.dtypes)

    for i in range(len(us_holiday.index)):
        for j in range(len(calendar_df.index)):
            if calendar_df.iloc[j, -1] == us_holiday.iloc[i, 0]:
                calendar_df.iloc[j, 4] = us_holiday.iloc[i, 1]

    return calendar_df


def get_countdown(calendar_df):
    today = datetime.today()

    for i in range(len(calendar_df.index)):
        delta = calendar_df['Date_Datetime'][i] - today
        calendar_df.iloc[i, 5] = delta.days

    return calendar_df

def init_calendar():
    base_df = base_calendar('2023-01-01', '2023-12-31')

    day_df = get_day(base_df)
    # print(day_df.head())
    lunar_df = lunar_auspicious_dates_2023(day_df)
    # print(lunar_df.head())

    hindu_df = hindu_auspicious_dates_2023(lunar_df)
    # print(hindu_df)
    countdown_df = get_countdown(hindu_df)
    # print(countdown_df)
    US_holiday_df = get_US_holiday(countdown_df)
    # print(US_holiday_df)

    # clean up and delete the last column

    index_list = US_holiday_df['Date']
    calendar_2023_df = US_holiday_df.drop(columns=['Date_Datetime'])
    calendar_2023_df.index = index_list
    return calendar_2023_df

if __name__ == '__main__':
    base_df = base_calendar('2023-01-01', '2023-12-31')

    day_df = get_day(base_df)
    # print(day_df.head())
    lunar_df = lunar_auspicious_dates_2023(day_df)
    # print(lunar_df.head())

    hindu_df = hindu_auspicious_dates_2023(lunar_df)
    # print(hindu_df)
    countdown_df = get_countdown(hindu_df)
    # print(countdown_df)
    US_holiday_df = get_US_holiday(countdown_df)
    # print(US_holiday_df)

    # clean up and delete the last column
    index_list = US_holiday_df['Date']
    calendar_2023_df = US_holiday_df.drop(columns=['Date_Datetime'])
    calendar_2023_df.index = index_list
    # print(calendar_df)

    # write to output
    calendar_2023_df.to_csv("output.csv")
