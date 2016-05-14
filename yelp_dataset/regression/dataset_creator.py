#!/usr/bin/env python

import csv
import json
from itertools import izip

new_csv_headers = ['business_id', 'stars', 'takeout', 'drivethru', 'outdoorseating', 'caters', 'noise', 'delivery', 'attire', 'gf_dinner', 'reservations', 'classy', 'waiter', 'alcohol', 
'Sandwiches', 'Bars', 'Chinese', 'Dessert', 'Italian', 'Cafes', 'Mediterranean', 'Japanese', 'French', 'Food Trucks', 'Non-American', 'American', 'Non-White', 'Asian', 'Latin American', 'Thai', 'Brunch', 'Pizza', 'Korean', 'European']

def extractData(attribute_file, category_file):

	with open(attribute_file, 'rb') as fid, open(category_file, 'rb') as cf:

		reader1 = csv.reader(fid, delimiter='|')
		reader2 = csv.reader(cf)

		reader1.next()  # skip past first line
		reader2.next()

		good_inds = [1, 2, 3, 4, 5, 6, 12, 14, 19, 22, 25, 32, 36]
		price_ind = 13
		
		cheap_restaurants = []
		expensive_restaurants = []

		for row1, row2 in zip(reader1, reader2):

			assert row1[0] == row2[0]

			if row1[price_ind] == 'n/a':
				continue
			feat = []

			feat.append(row1[0])

			for i in good_inds:
				curr_val = row1[i]
				if i == 1:  # stars
					if curr_val == 'n/a':
						curr_val = 0
					else:
						curr_val = float(curr_val)
						# if float(curr_val) > 3.0:
						# 	curr_val = 1
						# else:
						# 	curr_val = 0
				elif i == 6:  # noise
					if curr_val in ['loud', 'very_loud']:
						curr_val = 1
					else:
						curr_val = 0
				elif i == 14:  # attire
					if curr_val in ['formal', 'dressy']:
						curr_val = 1
					else:
						curr_val = 0
				elif i == 36:  # alcohol
					if curr_val in ['beer_and_wine', 'full_bar']:
						curr_val = 1
					else:
						curr_val = 0
				else:
					assert curr_val in ['n/a', 'True', 'False']
					if curr_val == 'True':
						curr_val = 1
					else:
						curr_val = 0
				feat.append(curr_val)
			
			feat.extend(row2[1:])

			price = int(row1[price_ind])
			if price > 2:
				expensive_restaurants.append(feat)
			else:
				cheap_restaurants.append(feat)

	return cheap_restaurants, expensive_restaurants
	
def main():
	cr, er = extractData('../cleaned_data/attributes_all.txt', 'restaurant_with_updated_categories.csv')

	with open('expensive_restaurants.csv', 'wb') as e:
		writer = csv.writer(e)

		writer.writerow(new_csv_headers)

		for entry in er:
			writer.writerow(entry)

	with open('cheap_restaurants.csv', 'wb') as c:
		writer = csv.writer(c)

		writer.writerow(new_csv_headers)

		for entry in cr:
			writer.writerow(entry)

if __name__ == '__main__':
	main()
