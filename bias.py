"""
One at a time, measures the difference across average review scores between websites.
So far, absolutely no filtering is done on the data. 
Scores will be normalized to be out of 5 to fit the Yelp data (i.e. Foursquare will be divided by 2).
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
    filename = "data/opentable_csvs/" + line[0] + ".csv"
    stars += otread(filename)

ostars = (stars/count)

print "OPENTABLE: " + str(round(ostars, 2))


#######FILTERED BY DOLLAR SIGN

#######FILTERED BY GENRE


