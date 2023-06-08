# File: global_variables.py
# This file stores the state_id and city_id some websites use in their URLs to identify the state and the city.
# Also initializes the dataframes we use in our codes.
# Imported by app.py, venue.py

import pandas as pd

location = {'Alabama' : ('Birmingham', 10064, 'g30375', 'Montgomery', 10078, 'g30712'),
 			'Alaska' : ('Anchorage', 10083, 'g60880'),
 			'Arizona' : ('Phoenix', 10086, 'g31310', 'Tucson', 10092, 'g60950'),
 			'Arkansas' : ('Little Rock', 10077, 'g60766'),
 			'California' : ('Fresno', 10098, 'g32414', 'Inland Empire', 10099, 'null', 'Los Angeles', 10095, 'g32655',
 				'Monterey', 10101, 'g32737', 'Napa Valley', 10102, 'g580460', 'Orange County', 10096, 'g659482',
 				'Sacramento', 10108, 'g32999', 'San Diego', 10106, 'g60750','San Francisco', 10100, 'g60713',
 				'Santa Barbara', 10097, 'g33045'),
 			'Colorado' : ('Denver', 10085, 'g33388'),
 			'Connecticut' : ('Hartfor', 10028, 'g33804'),
 			'Delaware' : ('Wilmington', 10036, 'g49673'),
 			'District of Columbia' : ('Washington DC', 10014, 'g28970'),
 			'Florida' : ('Florida Keys', 10025, 'g34340', 'Jacksonville', 10044, 'g60805', 'Miami', 10024, 'g34438',
 				'Naples', 10050, 'g34467', 'Orlando', 10029, 'g34515', 'Panhandle', 10076, 'g1438845',
 				'Tallahassee', 10026, 'g34675', 'Tampa', 10032, 'g34678'),
 			'Georgia' : ('Atlanta', 10022, 'g60898', 'Columbus', 10020, 'g50226', 'Savannah', 10011, 'g60814'),
 			'Hawaii' : ('Big Island', 76, 'g29217', 'Kauai', 77, 'g29218', 'Lanai', 78, 'g29219', 
 				        'Maui', 79, 'g29220', 'Oahu' ,81, 'g29222'),
 			#region_id = 10084; geozone_id = 76, 77, 78, 79, 81
 			'Idaho' : ('Boise', 10088, 'g35394'),
 			'Illinois' : ('Chicago', 10052, 'g35805', 'Chicago Suburbs', 10110, 'null', 'Springfield', 10070, 'null'),
 			'Indiana' : ('Indianapolis', 10023, 'g37209', 'South Bend', 10111, 'g37535'),
 			'Iowa' : ('Cedar Rapids', 10067, 'g37743', 'Des Moines', 10075, 'g37835'),
 			'Kansas' : ('Topeka', 10053, 'g60747', 'Wichita', 10074, 'g39143'),
 			'Kentucky' : ('Bowling Green', 10065, 'g39214', 'Lexington', 10033, 'g39588'),
 			'Louisiana' : ('New Orleans', 10062, 'g60864', 'Shreveport', 10055, 'g40424'),
 			'Maine' : ('Portland', 10000, 'g40827'),
 			'Maryland' : ('Baltimore', 10015, 'g60811'),
 			'Massachusetts' : ('Boston', 10008, 'g60745', 'Cape Cod', 10009, 'g185492', 'Springfield', 10034, 'g60968'),
 			'Michigan' : ('Detroit', 10007, 'g42139', 'Grand Rapids', 10045, 'g42256'),
 			'Minnesota' : ('Minneapolis', 10056, 'g43323'),
 			'Mississippi' : ('Jackson', 10079, 'g43833'),
 			'Missouri' : ('Kansas City', 10057, 'g44535', 'Springfield', 10061, 'g44926', 'St. Louis', 10054, 'g44881'),
 			'Montana' : ('Bozeman', 10087, 'g45095'),
 			'Nebraska' : ('Omaha', 10080, 'g60885'),
 			'Nevada' : ('Los Vegas', 10107, 'g45963', 'Reno', 10103, 'g45992'),
 			'New Hampshire' : ('Concord', 10010, 'g46052'),
 			'New Jersey' : ('Central Jersey', 10112, 'null', 'Jersey Shore', 10113, 'g659474',
 				'Northern New Jersey', 10001, 'g28951', 'Southern New Jersey', 10005, 'g28951'),
 			'New Mexico' : ('Albuquerque', 10093, 'g60933'),
 			'New York' : ('Albany', 10027, 'g29786' , 'Buffalo', 10016, 'g60974', 'Greater NYC Metro', 10114, 'null',
 				'Long Island', 10003, 'g1501343', 'New York City', 10002, 'g60763', 'Syracuse', 10037, 'g187891',
 				'Westchester County', 10004, 'g48865'),
 			'North Carolina' : ('Charlotte', 10018, 'g49022', 'Outer Banks', 10042,'g616326',
 				'Raleigh', 10041, 'g49463', 'Wilmington', 10043, 'g49673'),
 			'North Dakota' : ('Fargo', 10081, 'g49785'),
 			'Ohio' : ('Cincinnati', 10017, 'g60993', 'Cleveland', 10013, 'g50207', 
 				      'Columbus', 10030, 'g50226', 'Toledo', 10031, 'g51048'),
 			'Oklahoma' : ('Oklahoma City', 10071, 'g51560', 'Tulsa', 10073, 'g51697'),
 			'Oregon' : ('Eugene', 10094, 'g51862', 'Portland', 10105, 'g52024'),
 			'Pennsylvania' : ('Lancaster', 10047, 'g52970', 'Philadelphia', 10006, 'g60795',
 				'Pittsburgh', 10012, 'g53449', 'Scranton', 10051, 'g60969'),
 			'Rhode Island' : ('Providence', 10019, 'g60946'),
 			'South Carolina' : ('Charleston', 10048, 'g54171', 'Columbia', 10035, 'g54184', 'Hilton Head', 10049, 'g54273'),
 			'South Dakota' : ('Sioux Falls', 10082, 'g54805'),
 			'Tennessee' : ('Knoxville', 10040, 'g55138', 'Memphis', 10068, 'g55197', 'Nashville', 10072, 'g55229'),
 			'Texas' : ('Austin', 10066, 'g30196', 'Dallas', 10063, 'g55711', 'El Paso', 10089, 'g60768',
 				'Houston', 10060, 'g56003', 'San Antonio', 10069, 'g60956'),
 			'Utah' : ('Salt Lake City', 10091, 'g60922'),
 			'Vermont' : ('Burlington', 10021, 'g57201'),
 			'Virginia' : ('Hampton Roads', 10039, 'null', 'Richmond', 10038, 'g60893'),
 			'Washington' : ('Seattle', 10104, 'g60878', 'Spokane', 10109, 'g58759'),
 			'West Virginia' : ('Charleston', 10046, 'g58947'),
 			'Wisconsin' : ('Green Bay', 10059, 'g59929', 'Milwaukee', 10058, 'g60097'),
 			'Wyoming' : ('Cheyenne', 10090, 'g60439')}

state =  dict(zip(location.keys(),[x for x in range(400,451)]))

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

calendar_2023_df = pd.DataFrame()










