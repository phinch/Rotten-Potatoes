from lxml import html
import requests
import math
import csv

page = requests.get('http://www.opentable.com/s/restaurantlist?metroid=7&regionids=92&neighborhoodids=670')
tree = html.fromstring(page.content)

# Creates list of all restaurant names
names = []

# Creates list of all restaurant urls
restaurant_urls = tree.xpath('//*[@id="search_results"]/div/div/div[1]/div[2]/a/@href')

# Iterate through list of names and store in dictionary mapping name to list reviews
name_to_reviews = {}

for i in range(len(restaurant_urls) - 1):
	to_add = []

	base_url = 'http://www.opentable.com/' + restaurant_urls[i]

	page = requests.get(base_url)
	tree = html.fromstring(page.content)

	# Find total number of reviews
	num_reviews = tree.xpath('//*[@id="reviews-page"]/div/div[1]/text()')

	# If it has no reviews, continue
	if num_reviews == []:
		continue

	# Only do everything else if the restaurant has reviews

	# Find number of reviews
	num_reviews = int("".join(x for x in num_reviews[0] if x.isdigit()))

	#Add name to the list
	name = tree.xpath('//*[@id="info"]/div[1]/h3/text()')
	name = name[0][6:]
	names.append(name)

	print name
	print num_reviews

	# We know that there are 40 reviews per page, so use total reviews to determine num iterations
	num_loops = math.ceil(num_reviews/40.0)
	# Cast to int to pass into range function
	num_loops = int(num_loops)
	
	restaurant_titles = []
	restaurant_review_text = []
	restaurant_review_date = []
	restaurant_review_score = []

	for j in range(num_loops):
		
		# Set URL based on page
		url = base_url + '?page=' + str(j + 1)

		page = requests.get(url)
		tree = html.fromstring(page.content)

		# Grab all the Review Titles, Text, Date, and Score
		titles = tree.xpath('//*[@id="reviews-results"]/div/div/div[2]/div/h4/text()')
		review_text = tree.xpath('//*[@id="reviews-results"]/div/div/div[2]/div/div[2]/p/text()')
		review_date = tree.xpath('//*[@id="reviews-results"]/div/div/div[2]/div/div[1]/span/text()')
		review_score = tree.xpath('//*[@id="reviews-results"]/div/div/div[1]/div/div[1]/div/div/div[2]/@title')

		# Trim review date to get "February 20, 2016" from "Dined on February 20, 2016"
		for k in range(len(review_date) - 1):
			review_date[k] = review_date[k][9:]

		#Add everything to a new list
		restaurant_titles.extend(titles)
		restaurant_review_text.extend(review_text)
		restaurant_review_date.extend(review_date)
		restaurant_review_score.extend(review_score)

	name_to_reviews[name] = (restaurant_titles, restaurant_review_text, restaurant_review_date, restaurant_review_score)

# Open Files
names_file = open("data/opentable_names.txt", "wb")

print "Len names: " + str(len(names))

# Loop through name_to_reviews and write to file
for i in range(len(names) - 1):

	name = names[i]

	# Write restaurant name to names_file
	names_file.write('data/opentable_csvs/'+ name + '\n')

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
