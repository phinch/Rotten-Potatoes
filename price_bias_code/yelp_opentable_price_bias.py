import math
import csv

f = open('../opentable_matches_with_yelp.txt', 'r')
g = open('../yelp_matches_with_opentable.txt', 'r')

yelp_reader = csv.reader(open('../data/yelp_providence/yelp_pg.csv', 'rb'), delimiter = "|")
opentable_reader = csv.reader(open('../data/opentable_pg/opentable_pg.csv', 'rb'), delimiter = "|")

next(yelp_reader, None)
next(opentable_reader, None)

y_pt1 = []
y_pt2 = []
y_pt3 = []

ot_pt1 = []
ot_pt2 = []
ot_pt3 = []

# name -> price, rating, review count
yelp_data = {}
opentable_data = {}

for line in opentable_reader: # Name|Price|Genre|Rating|Review Count
	opentable_data[line[0]] = (float(line[1]), float(line[3]), float(line[4]))

for line in yelp_reader: # Name|Price|Genres|Rating|Review Count|Address
	if line[1] == 'N/A':
		continue
	yelp_data[line[0]] = (float(line[1]), float(line[3]), float(line[4]))

for frest in f:
	f_trim = frest.replace("\n", "")
	grest = g.readline()
	g_trim = grest.replace("\n", "")
	if f_trim in opentable_data and g_trim in yelp_data:
		ftup = opentable_data[f_trim]
		gtup = yelp_data[g_trim]
		prange = (ftup[0] + gtup[0]) / 2
		if prange < 2:
			y_pt1.append(gtup)
			ot_pt3.append(ftup)
		elif prange < 3:
			y_pt2.append(gtup)
			ot_pt2.append(ftup)
		else:
			y_pt3.append(gtup)
			ot_pt3.append(ftup)

sumrats = 0
sumrevs = 0

for elt in y_pt1:
	sumrats += elt[1] * elt[2]
	sumrevs += elt[2]

if sumrevs == 0:
	yelp1 = "n/a"
else:
	yelp1 = sumrats / sumrevs

sumrats = 0
sumrevs = 0

for elt in ot_pt1:
	sumrats += elt[1] * elt[2]
	sumrevs += elt[2]

if sumrevs == 0:
	ot1 = "n/a"
else:
	ot1 = sumrats / sumrevs

sumrats = 0
sumrevs = 0

for elt in y_pt2:
	sumrats += elt[1] * elt[2]
	sumrevs += elt[2]

if sumrevs == 0:
	yelp2 = "n/a"
else:
	yelp2 = sumrats / sumrevs

sumrats = 0
sumrevs = 0

for elt in ot_pt2:
	sumrats += elt[1] * elt[2]
	sumrevs += elt[2]

if sumrevs == 0:
	ot2 = "n/a"
else:
	ot2 = sumrats / sumrevs

sumrats = 0
sumrevs = 0

for elt in y_pt3:
	sumrats += elt[1] * elt[2]
	sumrevs += elt[2]

if sumrevs == 0:
	yelp3 = "n/a"
else:
	yelp3 = sumrats / sumrevs

sumrats = 0
sumrevs = 0

for elt in ot_pt3:
	sumrats += elt[1] * elt[2]
	sumrevs += elt[2]

if sumrevs == 0:
	ot3 = "n/a"
else:
	ot3 = sumrats / sumrevs

print str(yelp1) + " and " + str(ot1)
print str(yelp2) + " and " + str(ot2)
print str(yelp3) + " and " + str(ot3)