import json
from lxml import html
import requests
import math
import csv

# JSON format
# {
#     'type': 'business',
#     'business_id': (encrypted business id),
#     'name': (business name),
#     'neighborhoods': [(hood names)],
#     'full_address': (localized address),
#     'city': (city),
#     'state': (state),
#     'latitude': latitude,
#     'longitude': longitude,
#     'stars': (star rating, rounded to half-stars),
#     'review_count': review count,
#     'categories': [(localized category names)]
#     'open': True / False (corresponds to closed, not business hours),
#     'hours': {
#         (day_of_week): {
#             'open': (HH:MM),
#             'close': (HH:MM)
#         },
#         ...
#     },
#     'attributes': {
#         (attribute_name): (attribute_value),
#         ...
#     },
# }

url_base = "http://www.yelp.com/biz/"

data = []

# with open('restaurants.json') as f:
#     for line in f:
#         data.append(json.loads(line))
with open('test.json') as f:
    for line in f:
        data.append(json.loads(line))

# cities = []

with open("business.txt", "wb") as r:
	# with open("restaurants.json", "wb") as s:
	r.write("business_id|name|city|state|latitude|longitude|stars|review_count|price|genres\n")
	for elt in data:
		business_id = elt['business_id'].encode("utf-8")
		name = elt['name'].encode("utf-8")
		city = elt['city'].encode("utf-8")
		state = elt['state'].encode("utf-8")
		latitude = elt['latitude']
		longitude = elt['longitude']
		stars = elt['stars']
		review_count = elt['review_count']
		categories = elt['categories']
		street_addr = elt['full_address'].split("\n")[0]

		genres = ""
		for c in range(0,len(categories)):
			if categories[c] != "Restaurants":
				genres += categories[c]
			if (c != len(categories)-1) and (categories[c+1] != "Restaurants"):
				genres += ","

		# json.dump(elt, s)
		# s.write("\n")

		# cities.append(city)
			
		'''
		NOTES ON URLs:
		general rule: base url + name components separated by '-' + city name
		strip apostrophes - possessives, keep together; others (ex. D'Oro), strip and space separate SOMETIMES (ex. exception: Eat'n Park -> eat n)
		replace ampersands with 'and'
		chain restaurant urls - must iterate through appended index at end until address matches
		periods with no space (ex. P.F. Changs) - strip punctuation and space separate
		dashes (ex. co-op) - leave as is
		numbers (ex. No 1 China House) - leave as is
		restaurants with locational specifiers (ex. Mad Mex - South Hills) - take away spaces on either side of the dash
		special characters - utf-8 encoding handles this I believe
		extra space at end (ex. Lot 17 ) - delete
		'''

	# city_set = set(cities)
	# for c in city_set:
	# 	print c

		# clean restaurant names
		url_additives = [] # accounts for apostrophe anomalies

		url_additive = ""
		idx = 0
		while idx < len(name):
			toAdd = 0
			if name[idx] == '&':
				url_additive += "and"
			elif (name[idx] == ' ') and (idx <= len(name)-3) and (name[idx+1] == '-') and (name[idx+2] == ' '):
				toAdd = 2
				url_additive += "-"
			elif (name[idx] == ' ') and (idx != len(name)-1) and (name[idx+1] != ' '):
				url_additive += "-"
			elif (name[idx] == '.') and (idx != len(name)-1) and (name[idx+1] != ' '):
				url_additive += "-"
			elif (name[idx] == '.') and (idx != len(name)-1) and (name[idx+1] == ' '):
				toAdd = 1
				url_additive += "-"	
			elif (name[idx] == ' ') and (idx == len(name)-1):
				idx += 1
				continue
			elif (name[idx] == '\'') and (idx != len(name)-1):
				idx += 1
				continue
				# TODO: add support for apostrophe to dash (line 48)
			elif name[idx] == '!':
				continue
			else:
				url_additive += name[idx]

			idx = idx + 1 + toAdd

		url_additives.append(url_additive + "-")

		'''
		NOTES ON CITIES:
		if there is a slash (ex. Pittsburgh/Waterfront) - replace with '-'
		apostrophes (ex. L'Ile) - replace with '-'
		multiword with parentheses (ex. Weingarten (Baden)) - take away parentheses, separate with '-'
		periods (ex. Ft. Mill) - delete
		'''

		# clean city names
		clean_city = ""
		c_idx = 0
		while c_idx < len(city):
			idx_Add = 0
			if city[c_idx] == '/':
				clean_city += "-"
			elif city[c_idx] == '\'':
				clean_city += "-"
			elif city[c_idx] == '.':
				idx_Add = 1
				clean_city += "-"
			elif (city[c_idx] == '(') or (city[c_idx] == ")"):
				continue
			elif (city[c_idx] == ' ') and (c_idx != len(city)-1):
				clean_city += "-"
			elif (city[c_idx] == ' ') and (c_idx == len(city)-1):
				continue	
			else:
				clean_city += city[c_idx]

			c_idx = c_idx + 1 + idx_Add

		# append cleaned city names to the end of the url additive
		full_urls = []
		for u in url_additives:
			full_urls.append(u + clean_city)

		# TODO: add support for appending numbers to the url for chain restaurants
		numIters = 1 # the number to append to the end of the link (chain restaurants)

		pageFound = False

		while not(pageFound): # and (numIters <= 10):		
			for url_to_try in full_urls:
				pagelink = url_base + url_to_try
			  	page = requests.get(pagelink)
			  	tree = html.fromstring(page.content)

			 	street = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/span/li/strong/address/span[1]/text()')
		        
		       	if street == []:
		        	street = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]/div/div[2]/ul/span/li/strong/address/span[1]/text()')

		        # check to ensure correct location
		        if street != []:
		        	if street[0] == street_addr:
		        		pageFound = True

				price = ""
				p = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div/div[2]/span[1]/span/text()')
				if p == []:
					price = "N/A"
				else:
					price = str(len(p[0]))

		toAppend = business_id + "|" + name + "|" + city + "|" + state + "|" + str(latitude) + "|" + str(longitude) + "|" + str(stars) + "|" + str(review_count) + "|" + price + "|" + genres + "\n"
		r.write(toAppend)