import json
import math
import csv

price = dict()

with open('business.txt') as f:
	f.readline()
	for line in f:
		cpts = line.split("|")
		if cpts[8] in price:
			price[cpts[8]].append(cpts[10])
		else:
			price[cpts[8]] = [cpts[10]]

	avgs = dict()

	for key in price:
		sum_scores = 0.0
		num_scores = 0
		for elt in price[key]:
			if elt != 'N/A\n':
				num_scores += 1
				sum_scores += float(elt)
		avgs[key] = sum_scores/float(num_scores)

	for key in avgs:
		print key + " -> " + str(avgs[key])
