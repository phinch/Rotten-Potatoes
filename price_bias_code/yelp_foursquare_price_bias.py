import math
import csv

data_reader = csv.reader(open('../data/name_matches/yelp_foursquare.csv', 'rb'), delimiter = "|")

next(data_reader, None)

y_pt1 = []
y_pt2 = []
y_pt3 = []

fs_pt1 = []
fs_pt2 = []
fs_pt3 = []

for line in data_reader: # Name|Price Average|Genres|Yelp Score|Yelp Count|FS Score|FS Count
	if line[1] == "N/A":
		continue
	prange = float(line[1])
	if prange < 2:
		y_pt1.append((float(line[3]), float(line[4])))
		fs_pt1.append((float(line[5]), float(line[6])))
	elif prange < 3:
		y_pt2.append((float(line[3]), float(line[4])))
		fs_pt2.append((float(line[5]), float(line[6])))
	else:
		y_pt3.append((float(line[3]), float(line[4])))
		fs_pt3.append((float(line[5]), float(line[6])))

sumrats = 0
sumrevs = 0

for elt in y_pt1:
	sumrats += elt[0] * elt[1]
	sumrevs += elt[1]

if sumrevs == 0:
	yelp1 = "n/a"
else:
	yelp1 = sumrats / sumrevs

sumrats = 0
sumrevs = 0

for elt in fs_pt1:
	sumrats += elt[0] * elt[1]
	sumrevs += elt[1]

if sumrevs == 0:
	fs1 = "n/a"
else:
	fs1 = sumrats / sumrevs

sumrats = 0
sumrevs = 0

for elt in y_pt2:
	sumrats += elt[0] * elt[1]
	sumrevs += elt[1]

if sumrevs == 0:
	yelp2 = "n/a"
else:
	yelp2 = sumrats / sumrevs

sumrats = 0
sumrevs = 0

for elt in fs_pt2:
	sumrats += elt[0] * elt[1]
	sumrevs += elt[1]

if sumrevs == 0:
	fs2 = "n/a"
else:
	fs2 = sumrats / sumrevs

sumrats = 0
sumrevs = 0

for elt in y_pt3:
	sumrats += elt[0] * elt[1]
	sumrevs += elt[1]

if sumrevs == 0:
	yelp3 = "n/a"
else:
	yelp3 = sumrats / sumrevs

sumrats = 0
sumrevs = 0

for elt in fs_pt3:
	sumrats += elt[0] * elt[1]
	sumrevs += elt[1]

if sumrevs == 0:
	fs3 = "n/a"
else:
	fs3 = sumrats / sumrevs

print str(yelp1) + " and " + str(fs1)
print str(yelp2) + " and " + str(fs2)
print str(yelp3) + " and " + str(fs3)