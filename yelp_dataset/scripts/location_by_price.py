import json
import math
import csv
import operator

price = dict()

with open('../cleaned_data/business.txt') as f:
	f.readline()
	for line in f:
		cpts = line.split("|")
		if cpts[8] in price:
			price[cpts[8]].append(cpts[3])
		else:
			price[cpts[8]] = [cpts[3]]

	locs = dict()

	total_locs = dict()

	for key in price:
		locs_occ = dict()
		for elt in price[key]:
			if elt in locs_occ:
				locs_occ[elt] = locs_occ[elt] + 1
			else:
				locs_occ[elt] = 1
			if elt in total_locs:
				total_locs[elt] = total_locs[elt] + 1
			else:
				total_locs[elt] = 1
		sorted_locs = sorted(locs_occ.items(), key=operator.itemgetter(1), reverse=True)
		locs[key] = sorted_locs

	for key in locs:
		print key + " -> "
		for l in locs[key]:
			print l
		print "\n"

	sorted_total = sorted(total_locs.items(), key=operator.itemgetter(1), reverse=True)

	for elt in sorted_total:
		print elt