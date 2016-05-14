"""
Searches Yelp and Foursquare addresses and matches them up.
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

    "Coffee and Tea": ["Cafes"],
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

yelpinfo = {}
matchdata = {} 

yelp_data = csv.reader(open('../data/yelp_providence/yelp_pg.csv', 'rb'), delimiter = "|")
next(yelp_data, None)
for line in yelp_data:
    yelpinfo[line[5]] = [line[0], line[1], line[2], line[3], line[4]]

foursquare_reader = csv.reader(open('../data/foursquare/foursquare.csv', 'rb'), delimiter = "|")
next(foursquare_reader, None)
for line in foursquare_reader:
    address = line[4].split(" Ste")[0]
    if address in yelpinfo:
        matchdata[address] = yelpinfo[address]
        matchdata[address] += [line[1], float(line[2])/2, line[3]]

#Data is now in order Address: Name, Yelp Price, Genres, Yelp Score, Yelp Count, FS Price, FS Score (normalized), FS Count

with(open('../data/name_matches/yelp_foursquare.csv', 'wb')) as r:
    rwriter = csv.writer(r, delimiter = "|")
    rwriter.writerow(["Name", "Price Average", "Genres", "Yelp Score", "Yelp Count", "FS Score", "FS Count"])

    for key in matchdata:
        restaurant = matchdata[key]
        name = restaurant[0]
        if restaurant[1] != "N/A" and restaurant[5] != "N/A":
            price = (float(restaurant[1]) + float(restaurant[5]))/2
        else:
            price = restaurant[1]
        genres = restaurant[2]
        yscore = restaurant[3]
        ycount = restaurant[4]
        fscore = restaurant[6]
        fcount = restaurant[7]
        rwriter.writerow([name, price, genres, yscore, ycount, fscore, fcount])
