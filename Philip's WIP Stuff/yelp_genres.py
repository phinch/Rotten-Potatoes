"""
Creates a dictionary of all biases and counts from the Yelp data.
"""
from lxml import html
import requests
import math
import csv
import json

yelp_reader = csv.reader(open('../data/yelp_providence/yelp_pg.csv', 'rb'), delimiter = "|")
next(yelp_reader, None)

genres = {}

for line in yelp_reader: #Name|Price|Genres|Rating|Review Count
    restaurant = line[2].split(" /// ")
    for genre in restaurant:
        if genre in genres:
            genres[genre] += 1
        else:
            genres[genre] = 1

for key in genres:
    print key + "|" + str(genres[key])

