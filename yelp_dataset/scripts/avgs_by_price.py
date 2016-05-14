import json
import math
import csv

'''
Prints out star averages by price tier
'''

price = dict()

with open('../cleaned_data/business.txt') as f:
	f.readline()
	for line in f:
		cpts = line.split("|")
		if cpts[8] in price:
			price[cpts[8]].append((cpts[7],cpts[10]))
		else:
			price[cpts[8]] = [(cpts[7],cpts[10])]

	avgs = dict()

	for key in price:
		sum_scores = 0.0
		num_scores = 0
		for elt in price[key]:
			if elt[1] != 'N/A\n':
				num_scores += int(elt[0])
				sum_scores += float(elt[0])*float(elt[1])
		avgs[key] = sum_scores/float(num_scores)

	for key in avgs:
		print key + " -> " + str(avgs[key])
