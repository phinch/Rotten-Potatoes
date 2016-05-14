from lxml import html
import requests
import math
import csv

"""
Xpath for price: //*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div/div[2]/span[1]/span/text()
Xpath for genres: //*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div/div[2]/span[2]/a[XXXXXXXX]/text()
Xpath for name: //*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/h1/text()
Xpath for review: //*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/div/i/@title
Xpath for review count: //*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/span/span/text()

Note: Increment a from 1 upward until [] to retrieve all genres
"""

genre_base = '//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div/div[2]/span[2]/a['
genre_end = ']/text()'

url_base = "http://www.yelp.com/biz/"

reviews = {} #In form reviews[restaurant ID] = [score sum, number of reviews]

csv_reader = csv.reader(open('data/yelp_providence/restaurant_basic.txt', 'rb'), delimiter = "|")
next(csv_reader, None)

review_reader = csv.reader(open('data/yelp_providence/clean_reviews.txt', 'rb'), delimiter = "|")
for line in review_reader: #restaurant_id|user_id|rating|text|useful_votes|funny_votes|cool_votes
    restaurant = line[0]
    score = int(line[2])
    if restaurant in reviews:
        reviews[restaurant][0] += score
        reviews[restaurant][1] += 1
    else:
        reviews[restaurant] = [score, 1]
    

#NOTE: Genres in the csv will be separated by " /// " to match the csv format

with open("data/yelp_providence/yelp_pg.csv", "wb") as r:
    rwriter = csv.writer(r, delimiter = "|")
    rwriter.writerow(["Name", "Price", "Genres", "Rating", "Review Count", "Address"])

    for line in csv_reader:
        restaurant = line[0]
        name = line[1]
        pagelink = url_base + restaurant
        page = requests.get(pagelink)
        tree = html.fromstring(page.content)

        price = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div/div[2]/span[1]/span/text()')
        if price == []:
            price = "N/A"
        else:
            price = len(price[0])

        name = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/h1/text()')
        name = name[0].replace("\n", "")
        name = name.strip()

        if restaurant in reviews:
            score = round(float(reviews[restaurant][0]) / reviews[restaurant][1], 2)
            count = reviews[restaurant][1]
        else:
            score = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/div/i/@title')
            if score == []: 
                print "No score: ", name, price
                continue
            score = score[0].split()[0]

            count = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/span/span/text()')
            count = count[0]
        
        ###GENRES

        gcount = 1
        genres = ""
        genre = tree.xpath(genre_base+str(gcount)+genre_end)
        if genre == []:
            genres = "N/A"
        else:
            genres += genre[0]

            gcount += 1
            genre = tree.xpath(genre_base+str(gcount)+genre_end)
            while genre != []:
                genres += " /// "
                genres += genre[0]
                gcount += 1
                genre = tree.xpath(genre_base+str(gcount)+genre_end)

        address = ""

        street = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/span/li/strong/address/span[1]/text()')
        
        if street == []:
            street = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]/div/div[2]/ul/span/li/strong/address/span[1]/text()')

        if street == []:
            address = "n/a"
        else:
            address = street[0]

        print name.encode("utf-8"), price, genres, score, count, address

        rwriter.writerow([name.encode("utf-8"), price, genres, score, count, address])



