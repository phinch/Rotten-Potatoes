#!/usr/bin/env python
import csv
import sys
import string
import random
import numpy as np
from sklearn.metrics import accuracy_score
import porter_stemmer
import argparse

def main():
	wordbank = set()
	reviews = []
	labels = []
	
	print "importing reviews..."
	sys.stdout.flush()
	with open(feature_csv_path) as features:
		reader = csv.DictReader(features, delimiter='|')
		for row in reader:
			text = row['text']
			processedText = processText(text)
			words = processedText.split()
			#labeledReviews.append((row['positivity_label'], words))
			reviews.append(words)
			labels.append(int(row['positivity_label']))
			for word in words:
				wordbank.add(word)
				
	# Shuffle reviews and labels in unison
	tmp = list(zip(reviews, labels))
	random.shuffle(tmp)
	reviews, labels = zip(*tmp)
	
	#labels = np.array(labels, dtype='uint8')
	wordbank = list(wordbank)
	print "import complete."
	numWords = len(wordbank)
	numReviews = len(reviews)
	print numWords, "words in wordbank"
	print numReviews, "reviews to process"
	sys.stdout.flush()
	print "extracting features..."
	feats = extractFeatures(wordbank, reviews)
	print "running classifier..."
	sys.stdout.flush()
	acc = runClassifier(feats, labels, numWords, numReviews)
	print "accuracy:", acc
			
def runClassifier(feats, labels, numWords, numReviews):
	# set up train/test features/labels
	numLabels = numReviews
	numTrain = int(numLabels*0.8)
	trainLabels = labels[:numTrain]
	testLabels = labels[numTrain:]
	trainFeats = feats[:numTrain]
	testFeats = feats[numTrain:]
	print "extracting pos/neg feats..."
	sys.stdout.flush()
	trainPosFeats, trainNegFeats = getPosNegFeats(trainFeats, trainLabels, numWords, numTrain)
	print "finished extracting pos/neg feats."
	sys.stdout.flush()
	
	print "generating word probs..."
	sys.stdout.flush()
	
	if file_accessible('wordProbs.npy', 'r'):
		wordProbs = np.load('wordProbs.npy')
	else:
		wordProbs = np.zeros((numWords, 4)) # each row: [P(word|neg), P(^word|neg), P(word|pos), P(^word|pos)]
		numPosReviews = len(trainPosFeats)
		numNegReviews = len(trainNegFeats)
		assert(numNegReviews == numTrain - numPosReviews)
		for i in range(numWords):
			if i%100==0:
				print "generated {} out of {} word probs".format(i, numWords)
				sys.stdout.flush()
			N_pi = 0 # num positive reviews in which word i appears
			N_ni = 0 # num negative reviews in which word i appears
			for feat in trainPosFeats:
				if feat[i] == 1:
					N_pi += 1
			for feat in trainNegFeats:
				if feat[i] == 1:
					N_ni += 1
			pWordGivenPos = float(N_pi) / numPosReviews
			pNotWordGivenPos = 1 - pWordGivenPos
			pWordGivenNeg = float(N_ni) / numNegReviews
			pNotWordGivenNeg = 1 - pWordGivenNeg
			wordProbs[i,:] = np.array([pWordGivenNeg, pNotWordGivenNeg, pWordGivenPos, pNotWordGivenPos])
		if writeToFileMode:
			np.save('wordProbs', wordProbs)
	print "finished generating word probs."
	print "classifying..."
	sys.stdout.flush()
	return runLogClassifier(numWords, wordProbs, testFeats, testLabels)
	
def runLogClassifier(numWords, wordProbs, testFeats, testLabels):
	testSize = len(testFeats)
	labels = np.zeros(testSize, dtype='uint8')
	
	for i in range(testSize):
		if i%100 == 0:
			print "classified {} out of {}".format(i, testSize)
			sys.stdout.flush()
		pNeg = 0
		pPos = 0
		currReview = testFeats[i,:]
		for j in range(numWords):
			currWordProbs = wordProbs[j,:]
			pWordGivenNeg = currWordProbs[0]
			pNotWordGivenNeg = currWordProbs[1]
			pWordGivenPos = currWordProbs[2]
			pNotWordGivenPos = currWordProbs[3]
			if currReview[j] == 1:
				if pWordGivenNeg > 0:
					pNeg += np.log(pWordGivenNeg)
				if pWordGivenPos > 0:
					pPos += np.log(pWordGivenPos)
			elif currReview[j] == 0:
				if pNotWordGivenNeg > 0:
					pNeg += np.log(pNotWordGivenNeg)
				if pNotWordGivenPos > 0:
					pPos += np.log(pNotWordGivenPos)
		if pNeg > pPos:
			labels[i] = 0
		else:
			labels[i] = 1
	
	return accuracy_score(labels, testLabels)
	
def getPosNegFeats(feats, labels, numWords, numFeats):
	posFeats = []
	negFeats = []
	for i in range(numFeats):
		if labels[i] == 1:
			posFeats.append(feats[i])
		elif labels[i] == 0:
			negFeats.append(feats[i])
	posFeats = np.array(posFeats)
	negFeats = np.array(negFeats)
	return posFeats, negFeats
	
def extractFeatures(wordbank, reviews):
	if file_accessible('feats.npy', 'r'):
		return np.load('feats.npy')
	numWords = len(wordbank)
	numReviews = len(reviews)
	feats = np.zeros((numReviews, numWords), dtype='uint8')
	for review in enumerate(reviews):
		currRow = np.zeros(numWords, dtype='uint8')
		currInd = review[0]
		currText = review[1]
		if (currInd%100 == 0):
			print "extracted features from {} out of {} reviews".format(currInd, numReviews)
			sys.stdout.flush()
		for i in range(numWords):
			if wordbank[i] in currText:
				currRow[i] = 1
		feats[currInd,:] = currRow
	if writeToFileMode:
		np.save('feats', feats)
	return feats

def file_accessible(filepath, mode):
    ''' Check if a file exists and is accessible. '''
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False
    return True
				
def processText(text):
	# TODO: apply stemming, remove punctuation/stopwords, lowercase, etc.
	text = text.lower()
	text = removeStopwords(text)
	text = removePunc(text)
	text = stem(text)
	return text
	
def removePunc(text):
	replace_hyphen = string.maketrans('-', ' ')
	replace_comma = string.maketrans(',', ' ')
	replace_period = string.maketrans('.', ' ')
	text = text.translate(replace_hyphen) # replace all hyphens with a space (two words may be joined by a hyphen)
	text = text.translate(replace_comma)
	text = text.translate(replace_period)
	words = text.split()
	for i in range(len(words)):
		words[i] = words[i].translate(None, string.punctuation)
	return ' '.join(words)
	
def removeStopwords(text):
	with open(stopwords_path) as stopwords:
		stops = list(stopwords.read().splitlines())
	words = text.lower().split()
	words = [word for word in words if word not in stops]
	return ' '.join(words)
	
def stem(text):
	stemmer = porter_stemmer.PorterStemmer()
	words = text.lower().split()
	for i in range(len(words)):
		words[i] = stemmer.stem(words[i], 0, len(words[i])-1)
	return ' '.join(words)
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-feat', required=True, help='Path to feature csv')
	parser.add_argument('-stop', required=True, help='Path to stopwords')
	parser.add_argument('-write', type=bool, default=False, help='Enable if willing to write ~300mb of data to folder')
	opts = parser.parse_args()
	feature_csv_path = opts.feat
	stopwords_path = opts.stop
	writeToFileMode = opts.write
	#if len(sys.argv) != 3:
	#	print 'Usage: python review_classifier.py feature_csv_path stopwords_path'
	#	sys.exit()
	#feature_csv_path = sys.argv[1]
	#stopwords_path = sys.argv[2]
	main()