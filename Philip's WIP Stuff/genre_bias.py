"""
Measures bias between review sites organized by genre. 
Genres have been manually created by observing the data.
INITIAL DISPLAY:
    American
    Asian
    European
    Dessert
    Cafe
    Bar

OTHER CHOICES:
    Pizza
    Sandwiches+Deli
    Non-American
    Non-White
    Food Trucks
    Brunch
    Mediterannean
    Latin American
    French
    Italian
    Korean 
    Chinese
    Thai
    Japanese
"""
from lxml import html
import requests
import math
import csv
import json

def otread(name):
    ot_reader = csv.reader(open(name, 'rb'), delimiter = "|")
    next(ot_reader, None)
    stars = 0
    count = 0

    for line in ot_reader: #Review Title|Review Date|Review Score|Review Text
        count += 1
        stars += float(line[2])

    return stars/count

yelpset = []
fourset = []
openset = []

yelp_reader = csv.reader(open('data/yelp_providence/restaurant_info.txt', 'rb'), delimiter = "|")
for line in yelp_reader:
    yelpset += [line[0]]

###YELP
yelp_reader = csv.reader(open('data/yelp_providence/restaurant_info.txt', 'rb'), delimiter = "|")
next(yelp_reader, None)
count = 0
stars = 0

for line in yelp_reader: #name|latitude|longitude|stars|review_count|open
    count += 1
    stars += float(line[3])

ystars = stars/count

print "YELP: " + str(round(ystars, 2))

###FOURSQUARE
fs_reader = csv.reader(open('data/foursquare/foursquare.csv', 'rb'), delimiter = "|")
next(fs_reader, None)
count = 0
stars = 0

for line in fs_reader: #name|price|score|votes
    count += 1
    stars += float(line[2])

fstars = (stars/count)/2

print "FOURSQUARE: " + str(round(fstars, 2))

###TRIPADVISOR

###OPENTABLE
count = 0
stars = 0

opnames = csv.reader(open('data/opentable_names.txt', 'rb'), delimiter = "|")
for line in opnames:
    count += 1
    filename = line[0] + ".csv"
    stars += otread(filename)

ostars = (stars/count)

print "OPENTABLE: " + str(round(ostars, 2))


#######FILTERED BY DOLLAR SIGN

#######FILTERED BY GENRE


