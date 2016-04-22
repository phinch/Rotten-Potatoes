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

yfs_reader = csv.reader(open('../data/name_matches/yelp_foursquare.csv', 'rb'), delimiter = "|")
next(yfs_reader, None)

ytotal = 0
ytotalcount = 0
ftotal = 0
ftotalcount = 0

for line in yfs_reader: #Name|Price Average|Genres|Yelp Score|Yelp Count|FS Score|FS Count
    genres = line[2].split(" /// ")
    if genres[0] == "N/A":
        continue
    ycount = int(line[4])
    yscore = float(line[3])*ycount
    fcount = int(line[6])
    fscore = float(line[5])*fcount

    ytotal += yscore
    ytotalcount += ycount
    ftotal += fscore
    ftotalcount += fcount

    for genre in genres:
        if genre not in categories:
            continue
        else:
            maps = categories[genre]
            for category in maps:
                if category in scores:
                    scores[category][0] += yscore
                    scores[category][1] += ycount
                    scores[category][2] += fscore
                    scores[category][3] += fcount
                else:
                    scores[category] = [yscore, ycount, fscore, fcount]

#Total bias throughout the website
naturalbias = round(ytotal/ytotalcount - ftotal/ftotalcount, 2)

with(open('../data/bias_data/yelp_fs_bias.csv', 'wb')) as r:
    rwriter = csv.writer(r, delimiter = "|")
    rwriter.writerow(["Genre", "Yelp", "Foursquare", "Adjusted Bias", "Site Bias"])

    for genre in scores:
        info = scores[genre]
        yelp = info[0]/info[1]
        foursquare = info[2]/info[3]
        bias = round(yelp-foursquare, 2)
        rwriter.writerow([genre, round(yelp, 2), round(foursquare, 2), bias, naturalbias])



###YELP AND OPENTABLE
yelpdata = {}
otdata = {}
scores = {}

ydata_reader = csv.reader(open('../data/yelp_providence/yelp_pg.csv', 'rb'), delimiter = "|")
next(ydata_reader, None)

for line in ydata_reader: #Name|Price|Genres|Rating|Review Count|Address
    name = line[0]
    genres = line[2]
    rating = line[3]
    count = line[4]
    yelpdata[name] = [genres, rating, count]

ot_reader = csv.reader(open('../data/opentable_pg/opentable_pg.csv', 'rb'), delimiter = "|")
next(ot_reader, None)

for line in ot_reader: #Name|Price|Genre|Rating|Review Count
    name = line[0]
    rating = line[3]
    count = line[4]
    otdata[name] = [rating, count]

ynames_reader = csv.reader(open('../yelp_matches_with_opentable.txt', 'rb'))
otnames_reader = csv.reader(open('../opentable_matches_with_yelp.txt', 'rb'))

yname = ynames_reader.next()
otname = otnames_reader.next()

ytotal = 0
ytotalcount = 0
ottotal = 0
ottotalcount = 0

while yname[0] != "Paragon": #TODO
    if (otname[0] not in otdata) or (yname[0] not in yelpdata):
        print yname, otname
        yname = ynames_reader.next()
        otname = otnames_reader.next()
        continue
        
    opentable = otdata[otname[0]]
    yelp = yelpdata[yname[0]]

    genres = yelp[0].split(" /// ")
    if genres[0] == "N/A":
        yname = ynames_reader.next()
        otname = otnames_reader.next()
        continue

    ycount = int(yelp[2])
    yscore = float(yelp[1])*ycount

    otcount = int(opentable[1])
    otscore = float(opentable[0])*otcount

    ytotal += yscore
    ytotalcount += ycount
    ottotal = otscore
    ottotalcount = otcount

    for genre in genres:
        if genre not in categories:
            continue
        else:
            maps = categories[genre]
            for category in maps:
                if category in scores:
                    scores[category][0] += yscore
                    scores[category][1] += ycount
                    scores[category][2] += otscore
                    scores[category][3] += otcount
                else:
                    scores[category] = [yscore, ycount, otscore, otcount]

    yname = ynames_reader.next()
    otname = otnames_reader.next()

naturalbias = round(ytotal/ytotalcount - ottotal/ottotalcount, 2)

with(open('../data/bias_data/yelp_ot_bias.csv', 'wb')) as r:
    rwriter = csv.writer(r, delimiter = "|")
    rwriter.writerow(["Genre", "Yelp", "Opentable", "Adjusted Bias", "Site Bias"])

    for genre in scores:
        info = scores[genre]
        yelp = info[0]/info[1]
        opentable = info[2]/info[3]
        bias = round(yelp-opentable, 2)
        rwriter.writerow([genre, round(yelp, 2), round(opentable, 2), bias, naturalbias])

    

