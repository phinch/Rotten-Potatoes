#!/usr/bin/env python
import csv
import sys
import glob
import os

def main():
	csv_filenames = []
	score_reviews = []
	
	for file in glob.glob(data_path + '/*.csv'):
		csv_filenames.append(os.path.basename(file))

	for csv_filename in csv_filenames:
		with open(data_path + '/' + csv_filename) as reviews:
			reader = csv.DictReader(reviews, delimiter='|')
			for row in reader:
				text = row['Review Text']
				score = int(row['Review Score'])
				label = 1 # positive label
				if score < 3:
					label = 0 # negative label
				score_reviews.append((label, text))
	
	with open('features.csv', 'wb') as output:
		writer = csv.writer(output, delimiter='|')
		writer.writerow(['positivity', 'text'])
		for tup in score_reviews:
			writer.writerow([tup[0], tup[1]])

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: python feature_generator.py data_path'
		sys.exit()
	data_path = sys.argv[1]
	main()