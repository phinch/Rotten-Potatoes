from lxml import html
import requests
import math
import csv

page = requests.get('http://www.opentable.com/s/restaurantlist?metroid=7&regionids=92&neighborhoodids=670')
tree = html.fromstring(page.content)


# Creates list of all restaurant urls
restaurant_urls = tree.xpath('//*[@id="search_results"]/div/div/div[1]/div[2]/a/@href')

# Creates list of all restaurant types
genres = tree.xpath('//*[@id="search_results"]/div/div/div[1]/div[2]/div[3]/text()[1]')

for i in range(len(genres)):
    entry = genres[i]
    entry = entry.encode("utf-8")
    entry = entry.replace("\n","")
    entry = entry.strip()
    genres[i] = entry

# Creates list of restaurant prices
prices = tree.xpath('//*[@id="search_results"]/div/div/div[1]/div[2]/div[2]/i/text()')

for i in range(len(prices)):
    price = prices[i]
    price = price.encode("utf-8")
    price = price.replace("\n","")
    price = price.replace(" ", "")
    price = len(price)
    prices[i] = price

info_dict = {}

for i in range(len(restaurant_urls) - 1):
    to_add = []

    base_url = 'http://www.opentable.com/' + restaurant_urls[i]

    page = requests.get(base_url)
    tree = html.fromstring(page.content)

    # Find total number of reviews
    num_reviews = tree.xpath('//*[@id="reviews-toolbar"]/div[2]/text()')

    # If it has no reviews, continue
    if num_reviews == []:
        continue

    num_reviews = int(num_reviews[0].split()[0])

    # Only do everything else if the restaurant has reviews

    #Add name to the list
    name = tree.xpath('//*[@id="info"]/div[1]/h3/text()')
    name = name[0][6:]

    # We know that there are 40 reviews per page, so use total reviews to determine num iterations
    num_loops = math.ceil(num_reviews/40.0)
    # Cast to int to pass into range function
    num_loops = int(num_loops)
	
    review_count = 0
    score_total = 0
    
    for j in range(num_loops):
    	
        # Set URL based on page
        url = base_url + '?page=' + str(j + 1)

        page = requests.get(url)
        tree = html.fromstring(page.content)

        # Grab all the Review Titles, Text, Date, and Score
        review_score = tree.xpath('//*[@id="reviews-results"]/div/div/div[1]/div/div[1]/div/div/div[2]/@title')

        for score in review_score:
            review_count += 1
            score_total += float(score)

    average = round(score_total/review_count, 2)

    info_dict[name] = [prices[i], genres[i], average, review_count]
    print info_dict[name]

with open("data/opentable_pg/opentable_pg.csv", "wb") as r:
    rwriter = csv.writer(r, delimiter = "|")
    rwriter.writerow(["Name", "Price", "Genre", "Rating", "Review Count"])

    for key in info_dict:
        rwriter.writerow([key, info_dict[key][0], info_dict[key][1], info_dict[key][2], info_dict[key][3]])
        
"""
# Open File
pg = open("data/opentable_pg.csv", "wb")

print "Len names: " + str(len(names))

# Loop through name_to_reviews and write to file
for i in range(len(names) - 1):

	name = names[i]

	# Write restaurant name to names_file
	names_file.write(name + '\n')

	with open('data/opentable_csvs/' + name + '.csv', "wb") as r:
		rwriter = csv.writer(r, delimiter = '|')

		rwriter.writerow(["Review Title", "Review Date", "Review Score", "Review Text"])

		# Write review to restaurant file
		for j in range(len(name_to_reviews[name][0]) - 1):
			title = name_to_reviews[name][0][j]
			text = name_to_reviews[name][1][j]
			date = name_to_reviews[name][2][j]
			score = name_to_reviews[name][3][j]

			text = ' '.join(text.split())

			rwriter.writerow([date.encode('UTF-8'), title.encode('UTF-8'), score.encode('UTF-8'), text.encode('UTF-8')])

names_file.close()
"""
