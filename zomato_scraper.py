from lxml import html
from lxml import etree
import urllib2
import requests
import math
import csv

def extract_html(url):
    f = urllib2.urlopen(url)
    html_str = f.read()
    f.close()
    return html_str

url = 'https://www.zomato.com/providence/restaurants'
#f = urllib2.urlopen(url)
#html_str = f.read()
#f.close()

tree = html.fromstring(extract_html(url))

# list of all names
names = []

# list of restaurant urls
restaurant_urls = tree.xpath('//*[@id="orig-search-list"]/li/article/div/div/div/div/div/h3/a/@href')
print len(restaurant_urls)

for i in range(len(restaurant_urls)):
    print restaurant_urls[i]

name_to_reviews = {}

# TODO: extract restaurant reviews
for i in range(1):
    curr_url = restaurant_urls[i]
    print 'curr_url:', curr_url
    tree = html.fromstring(extract_html(curr_url))
    reviews = tree.xpath('//*[@id="reviews-container"]/div[1]/div[3]/div[1]/div[1]/div/div[3]/div[1]/text()')
    print reviews
