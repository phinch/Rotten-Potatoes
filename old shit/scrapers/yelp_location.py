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

url_base = "http://www.yelp.com/biz/"

csv_reader = csv.reader(open('../data/yelp_providence/restaurant_basic.txt', 'rb'), delimiter = "|")
next(csv_reader, None)

#NOTE: Genres in the csv will be separated by " /// " to match the csv format

with open("../data/yelp_providence/yelp_location.txt", "wb") as r:
    r.write("Name|Location\n")

    for line in csv_reader:
        restaurant = line[0]
        name = line[1]
        pagelink = url_base + restaurant
        page = requests.get(pagelink)
        tree = html.fromstring(page.content)

        address = ""

        street = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/span/li/strong/address/span[1]/text()')
        
        if street == []:
            street = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]/div/div[2]/ul/span/li/strong/address/span[1]/text()')
       
        city = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/span/li/strong/address/span[2]/text()')

        if city == []:
            city = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]/div/div[2]/ul/span/li/strong/address/span[2]/text()')
        
        region = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/span/li/strong/address/span[3]/text()')

        if region == []:
           region = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]/div/div[2]/ul/span/li/strong/address/span[3]/text()')

        zipcode = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/span/li/strong/address/span[4]/text()')

        if zipcode == []:
            zipcode = tree.xpath('//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]/div/div[2]/ul/span/li/strong/address/span[4]/text()')

        if street == [] or city == [] or region == [] or zipcode == []:
            address = "n/a"
        else:
            address = street[0] + ", " + city[0] + ", " + region[0] + " " + zipcode[0]

        r.write(name+"|"+address+"\n")



