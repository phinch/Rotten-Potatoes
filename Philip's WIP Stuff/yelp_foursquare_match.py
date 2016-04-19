"""
Searches Yelp and Foursquare addresses and matches them up.
"""
from lxml import html
import requests
import math
import csv
import json

yelpinfo = {}
matchdata = {} 

yelp_data = csv.reader(open('../data/yelp_providence/yelp_pg.csv', 'rb'), delimiter = "|")
next(yelp_data, None)
for line in yelp_data:
    yelpinfo[line[5]] = [line[0], line[1], line[2], line[3]]

foursquare_reader = csv.reader(open('../data/foursquare/foursquare.csv', 'rb'), delimiter = "|")
next(foursquare_reader, None)
for line in foursquare_reader:
    address = line[4].split(" Ste")[0]
    if address in yelpinfo:
        matchdata[address] = yelpinfo[address]
        matchdata[address] += [line[2]]

#Data is now in order Address: Name, Price Level, Genres, Yelp Score, FS Score

for key in matchdata:
    print matchdata[key]
        


