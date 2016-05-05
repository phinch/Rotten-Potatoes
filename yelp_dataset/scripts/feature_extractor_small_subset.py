import json
from lxml import html
import requests
import math
import csv

with open("../cleaned_data/philip.csv", "wb") as w:
    csvwriter = csv.writer(w)
    csvwriter.writerow(["price","reservations","attire","takeout"])

    with open('../data/restaurants.json') as f:
        for line in f:
            elt = json.loads(line)
            attributes = elt['attributes']

            if 'Take-out' in attributes:
                takeout = attributes['Take-out']
            else:
                takeout = False 
            if 'Price Range' in attributes:
                p = attributes['Price Range']
                if (p == 3) or (p == 4):
                    price = True
                else:
                    price = False
            else:
                price = False
            if 'Attire' in attributes:
                a = attributes['Attire']
                if a == 'casual':
                    attire = True
                else:
                    attire = False
            else:
                attire = False
            if 'Takes Reservations' in attributes:
                reservations = attributes['Takes Reservations']
            else:
                reservations = False
            
            csvwriter.writerow([price, reservations, attire, takeout])