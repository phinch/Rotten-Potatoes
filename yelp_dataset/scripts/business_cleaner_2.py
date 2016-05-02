import json
from lxml import html
import requests
import math
import csv

# JSON format
# {
#     'type': 'business',
#     'business_id': (encrypted business id),
#     'name': (business name),
#     'neighborhoods': [(hood names)],
#     'full_address': (localized address),
#     'city': (city),
#     'state': (state),
#     'latitude': latitude,
#     'longitude': longitude,
#     'stars': (star rating, rounded to half-stars),
#     'review_count': review count,
#     'categories': [(localized category names)]
#     'open': True / False (corresponds to closed, not business hours),
#     'hours': {
#         (day_of_week): {
#             'open': (HH:MM),
#             'close': (HH:MM)
#         },
#         ...
#     },
#     'attributes': {
#         (attribute_name): (attribute_value),
#         ...
#     },
# }

url_base = "http://www.yelp.com/biz/"

data = []
"""
# with open('restaurants.json') as f:
#     for line in f:
#         data.append(json.loads(line))
with open('test.json') as f:
    for line in f:
        data.append(json.loads(line))
"""
# cities = []

scores = {}
score_reader = csv.reader(open("../cleaned_data/review.txt", 'rb'), delimiter = "|")
next(score_reader, None)

for line in score_reader:
    bid = line[0]
    score = int(line[1])
    if bid not in scores:
        scores[bid] = [score, 1]
    else:
        scores[bid][0] += score
        scores[bid][1] += 1

with open("../cleaned_data/business.txt", "wb") as r:
    r.write("business_id|name|city|state|latitude|longitude|stars|review_count|price|genres|avg score\n")
    with open('../data/restaurants.json') as f:
        for line in f:
            elt = json.loads(line)
            business_id = elt['business_id'].encode("utf-8")
            name = elt['name'].encode("utf-8")
            city = elt['city'].encode("utf-8")
            state = elt['state'].encode("utf-8")
            latitude = elt['latitude']
            longitude = elt['longitude']
            stars = elt['stars']
            review_count = elt['review_count']
            categories = elt['categories']
            street_addr = elt['full_address'].split("\n")[0]

            if "Price Range" not in elt['attributes']:
                price = "N/A"
            else:
                price = elt['attributes']['Price Range']
            categories = elt['categories']

            genres = ""
            if categories == []:
                genres = "N/A"
            else:
                genres += categories[0].encode("utf-8")
                for i in range(1, len(categories)):
                    genres += " /// "
                    genres += categories[i].encode("utf-8")
            
            if business_id in scores:
                score = round(float(scores[business_id][0])/scores[business_id][1], 2)
            else:
                score = "N/A"

            toAppend = business_id + "|" + name + "|" + city + "|" + state + "|" + str(latitude) + "|" + str(longitude) + "|" + str(stars) + "|" + str(review_count) + "|" + str(price) + "|" + genres + "|" + str(score) + "\n"
            r.write(toAppend)
