#!/usr/bin/env python

import json
import csv

# this script creates a csv file for restaurants and gives business ids with all the new categories

new_categories_dict = {
					'Bars': 1, 
					'Chinese': 2, 
					'European': 19, 
					'Dessert': 3, 
					'Korean': 18, 
					'Cafes': 5, 
					'Mediterranean': 6, 
					'Japanese': 7, 
					'French': 8, 
					'Food Trucks': 9,
					'Non-American': 10,
					'American': 11, 
					'Non-White': 12, 
					'Sandwiches': 0,
					'Latin American': 14,
					'Pizza': 17,
				    'Thai': 15,
				    'Asian': 13,
			        'Brunch': 16,
			        'Italian': 4
			        }

new_categories_list = ['Sandwiches', 'Bars', 'Chinese', 'Dessert', 'Italian', 'Cafes', 'Mediterranean', 'Japanese', 'French', 'Food Trucks', 'Non-American', 'American', 'Non-White', 'Asian', 'Latin American', 'Thai', 'Brunch', 'Pizza', 'Korean', 'European']

categories = {
    "Sushi Bars": ["Japanese", "Asian", "Non-American", "Non-White"],
    "Japanese": ["Japanese", "Asian", "Non-American", "Non-White"],
    "Cantonese": ["Chinese", "Asian", "Non-American", "Non-White"],
    "Chinese": ["Chinese", "Asian", "Non-American", "Non-White"],
    "Thai": ["Thai", "Asian", "Non-American", "Non-White"],
    "Indian": ["Asian", "Non-American", "Non-White"],
    "Korean": ["Korean", "Asian", "Non-American", "Non-White"],
    "Pakistani": ["Asian", "Non-American", "Non-White"],
    "Mongolian": ["Asian", "Non-American", "Non-White"],
    "Asian Fusion": ["Asian", "Non-American", "Non-White"],
    "Vietnamese": ["Asian", "Non-American", "Non-White"],
    "Cambodian": ["Asian", "Non-American", "Non-White"],

    "French": ["French", "European", "Non-American"],
    "Creperies": ["French", "European", "Non-American"],
    "Italian": ["Italian", "European", "Non-American"],
    "Tapas/Small Plates": ["European", "Non-American"],
    "Tapas Bars": ["European", "Non-American"],
    "Irish": ["European", "Non-American"],
    "British": ["European", "Non-American"],
    
    "Bar": ["Bars"],
    "Dive Bar": ["Bars"],
    "Cocktail Bar": ["Bars"],
    "Dive Bars": ["Bars"],
    "Pub": ["Bars"],
    "Beer Bar": ["Bars"],
    "Bars": ["Bars"],
    "Pubs": ["Bars"],
    "Gastropubs": ["Bars"],
    "Wine Bars": ["Bars"],

    "Coffee & Tea": ["Cafes"],
    "Bubble Tea": ["Cafes"],
    "Cafes": ["Cafes"],
    "Cafe": ["Cafes"],
    "Juice Bar": ["Cafes"],

    "Steakhouses": ["American"],
    "American (New)": ["American"],
    "Breakfast and Brunch": ["Brunch", "American"],
    "Modern American": ["American"],
    "Traditional American": ["American"],
    "Steakhouse": ["American"],
    "Burgers": ["American"],
    "Diners": ["American"],
    "Fast Food": ["American"],
    "Hot Dogs": ["American"],
    "Seafood": ["American"],
    "American (Traditional)": ["American"],

    "Tex-Mex": ["Latin American", "Non-American", "Non-White"],
    "Cuban": ["Latin American", "Non-American", "Non-White"],
    "Cajun/Creole": ["Latin American", "Non-American", "Non-White"],
    "Latin American": ["Latin American", "Non-American", "Non-White"],
    "Mexican": ["Latin American", "Non-American", "Non-White"],

    "Mediterranean": ["Mediterranean", "Non-American", "Non-White"],
    "Moroccan": ["Mediterranean", "Non-American", "Non-White"],
    "Greek": ["Mediterranean", "Non-American", "Non-White"],
    "Middle Eastern": ["Mediterranean", "Non-American", "Non-White"],

    "Desserts": ["Dessert"],
    "Creperies": ["Dessert"],
    "Ice Cream & Frozen Yogurt": ["Dessert"],
    "Bakeries": ["Dessert"],
    "Bakery": ["Dessert"],
    "Donuts": ["Dessert"],

    "Bagels": ["Brunch"],

    "Food Stands": ["Food Trucks"],
    "Food Trucks": ["Food Trucks"],
    "Market Stall": ["Food Trucks"],

    "Ethiopian": ["Non-American", "Non-White"],

    "Pizza": ["Pizza"],
    "Sandwiches": ["Sandwiches"],
    "Delis": ["Sandwiches"]
}

def process_categories(curr_cat):
	toReturn = [0 for _ in range(20)]
	
	for c in curr_cat:

		if c in categories:

			new_categories = categories[c]
			for n in new_categories:
				index = new_categories_dict[n]
				toReturn[index] = 1

	return toReturn

write_file = open('restaurant_with_updated_categories.csv', 'wb')
writer = csv.writer(write_file)
writer.writerow(['business_id', 'Sandwiches', 'Bars', 'Chinese', 'Dessert', 'Italian', 'Cafes', 'Mediterranean', 'Japanese', 'French', 'Food Trucks', 'Non-American', 'American', 'Non-White', 'Asian', 'Latin American', 'Thai', 'Brunch', 'Pizza', 'Korean', 'European'])

with open('../data/restaurants.json', 'r') as r:
	for row in r:
		json_obj = json.loads(row)

		b_id = json_obj['business_id']
		curr_categories = json_obj['categories']
		new_categories = process_categories(curr_categories)

		toReturn = []
		toReturn.append(b_id)
		toReturn.extend(new_categories)

		writer.writerow(toReturn)

write_file.close()


