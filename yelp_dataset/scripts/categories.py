"""
Measures bias between review sites organized by genre. 
Genres have been manually created by observing the data.

"""
from lxml import html
import requests
import math
import csv
import json
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

#Score calculations: Multiply by number of reviewers. Ycount is a count of all Yelp reviewers

###YELP AND FOURSQUARE
scores = {} #Name of genre, [yscore, ycount, fscore, fcount]

biz_reader = csv.reader(open('../cleaned_data/business.txt', 'rb'), delimiter = "|")
next(biz_reader, None)

for line in biz_reader: #business_id|name|city|state|latitude|longitude|stars|review_count|price|genres|avg score
    genres = line[9].split(" /// ")
    count = int(line[7])
    if line[10] == "N/A":
        continue
    score = float(line[10])*count

    for genre in genres:
        if genre not in categories:
            continue
        else:
            done = []
            maps = categories[genre]
            for category in maps:
                if category in done:
                    continue
                else:
                    if category in scores:
                        scores[category][0] += score
                        scores[category][1] += count
                    else:
                        scores[category] = [score, count]
                    done += category


with(open('../cleaned_data/avg_by_genre.csv', 'wb')) as r:
    rwriter = csv.writer(r, delimiter = ",")
    rwriter.writerow(["Genre", "Average"])

    for genre in scores:
        info = scores[genre]
        rwriter.writerow([genre, round(info[0]/info[1], 2)])

