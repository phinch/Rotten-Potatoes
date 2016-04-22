"""
Calculates actual reviews for Yelp (instead of 
"""
from lxml import html
import requests
import math
import csv
import json

yelp_reader = csv.reader(open('../data/yelp_providence/yelp_pg.csv', 'rb'), delimiter = "|")
next(yelp_reader, None)

