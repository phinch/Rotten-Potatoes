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

csv_reader = csv.reader(open('data/yelp_providence/restaurant_basic.txt', 'rb'), delimiter = "|")
next(csv_reader, None)

#NOTE: Genres in the csv will be separated by " /// " to match the csv format

with open("data/yelp_providence/yelp_pg.csv", "wb") as r:
    rwriter = csv.writer(r, delimiter = "|")
    rwriter.writerow(["Name", "Price", "Genres", "Rating", "Review Count"])

    for line in csv_reader:
        restaurant = line[0]
        name = line[1]
        pagelink = url_base + restaurant
        page = requests.get(pagelink)
        tree = html.fromstring(page.content)

        price = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/ div[1]/div/div[2]/span[1]/span/text()')
        if price == []:
            price = "N/A"
        else:
            price = len(price[0])

        name = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/h1/text()')
        name = name[0].replace("\n", "")
        name = name.strip()

        score = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/div/i/@title')
        if score == []:
            continue
        score = score[0].split()[0]

        count = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/span/span/text()')
        count = count[0]

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

        print name.encode("utf-8"), price, genres, score, count

        rwriter.writerow([name.encode("utf-8"), price, genres, score, count])



