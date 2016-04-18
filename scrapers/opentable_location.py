from lxml import html
import requests
import math
import csv

page = requests.get('http://www.opentable.com/s/restaurantlist?metroid=7&regionids=92&neighborhoodids=670')
tree = html.fromstring(page.content)


# Creates list of all restaurant urls
restaurant_urls = tree.xpath('//*[@id="search_results"]/div/div/div[1]/div[2]/a/@href')

info_dict = {}

for i in range(len(restaurant_urls) - 1):
    base_url = 'http://www.opentable.com/' + restaurant_urls[i]

    page = requests.get(base_url)
    tree = html.fromstring(page.content)

    #Add name to the list
    name = tree.xpath('//*[@id="info"]/div[1]/h3/text()')
    name = name[0][6:]


    # Creates list of restaurant locations
    loc = tree.xpath('//*[@id="info"]/div[2]/div/div[2]/div/div/text()')

    location = loc[0] + ", " + loc[1]
    location = location.encode("utf-8")
    location = location.replace("  "," ")

    info_dict[name] = location
    print info_dict[name]

with open("../data/opentable_location.csv", "wb") as r:
    rwriter = csv.writer(r, delimiter = "|")
    rwriter.writerow(["Name", "Location"])

    for key in info_dict:
        rwriter.writerow([key, info_dict[key]])
        
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
