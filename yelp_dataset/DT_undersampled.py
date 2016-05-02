import csv
import random
import sys
import argparse
import numpy as np
from sklearn import tree
from sklearn import ensemble
from sklearn import cross_validation

def extractData(datapath):
	with open(datapath, 'rb') as fid:
		reader = csv.reader(fid, delimiter='|')
		reader.next()  # skip past first line
		good_inds = [1, 2, 3, 4, 5, 6, 12, 14, 19, 22, 25, 32, 36]
		price_ind = 13
		cheapX = []
		cheapY = []
		expX = []
		expY = []
		for row in reader:
			if row[price_ind] == 'n/a':
				continue
			feat = []
			for i in good_inds:
				curr_val = row[i]
				if i == 1:  # stars
					if curr_val == 'n/a':
						curr_val = 3.0  # average stars
					else:
						curr_val = float(curr_val)
				elif i == 6:  # noise
					if curr_val in ['loud', 'very_loud']:
						curr_val = 1
					else:
						curr_val = 0
				elif i == 14:  # attire
					if curr_val in ['formal', 'dressy']:
						curr_val = 1
					else:
						curr_val = 0
				elif i == 36:  # alcohol
					if curr_val in ['beer_and_wine', 'full_bar']:
						curr_val = 1
					else:
						curr_val = 0
				else:
					assert curr_val in ['n/a', 'True', 'False']
					if curr_val == 'True':
						curr_val = 1
					else:
						curr_val = 0
				feat.append(curr_val)
			price = row[price_ind]
			assert price != 'n/a'
			price = int(price)
			if price > 2:
				expX.append(feat)
				expY.append(1)
			else:
				cheapX.append(feat)
				cheapY.append(0)
	assert len(cheapX) == len(cheapY)
	assert len(expX) == len(expY)
	return cheapX, cheapY, expX, expY

def shuffleListPairs(X, Y):
	XY = zip(X, Y)
	random.shuffle(XY)
	return extractXY(XY)

def extractXY(XY):
	X = [i for i, j in XY]
	Y = [j for i, j in XY]
	return X, Y

def getUndersampledSets(smallX, smallY, bigX, bigY):
	bigTrainXY = random.sample(zip(bigX, bigY), len(smallY))
	bigTrainX, bigTrainY = extractXY(bigTrainXY)
	X = bigTrainX + smallX
	Y = bigTrainY + smallY
	return shuffleListPairs(X, Y)

def classifyWithUndersampling(clf, smallX, smallY, bigX, bigY):
	len_small = len(smallY)
	len_big = len(bigY)
	iter_weight = 3
	num_iter = int(float(len_big) / len_small) * iter_weight  # scale num_iter with big/small ratio
	accuracies = []
	# Undersample and obtain average score num_iter times, and then average together the average scores
	print 'Undersampling... (will sample/train/test %d cheap and %d expensive %d times)' % (len_small, len_small, num_iter)
	sys.stdout.flush()
	for _ in range(num_iter):
		X, Y = getUndersampledSets(smallX, smallY, bigX, bigY)
		scores = cross_validation.cross_val_score(clf, X, Y, cv=10)
		accuracies.append(scores.mean())
	accuracies = np.array(accuracies)
	print 'Finished!'
	print 'Accuracy: %0.2f%% (+/- %0.2f%%)' % (accuracies.mean()*100, accuracies.std()*2*100)

def generateDotFileWithUndersampling(clf, smallX, smallY, bigX, bigY):
	X, Y = getUndersampledSets(smallX, smallY, bigX, bigY)
	clf = clf.fit(X, Y)
	with open('DT_undersampled.dot', 'w') as f:
		tree.export_graphviz(clf, out_file=f)
	print 'Generated dot file'
	
def parseArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-classifier', required=True, help='dt or rf')
	parser.add_argument('-gendot', default=False, help='generate dot file')
	opts = parser.parse_args()
	classifier = opts.classifier
	gendot = opts.gendot
	if classifier not in ['dt', 'rf']:
		print 'Invalid classifier.'
		sys.exit(0)
	if gendot and classifier == 'rf':
		print 'gendot incompatible w/ random forest'
		sys.exit(0)
	return classifier, gendot

def main():  # TODO: parse user input to determine which classifier to run
	classifier, gendot = parseArgs()
	cheapX, cheapY, expX, expY = extractData('attributes_all.txt')
	print 'Num cheap restaurants:', len(cheapY)
	print 'Num expensive restaurants:', len(expY)
	if classifier == 'dt':
		clf = tree.DecisionTreeClassifier(max_depth=3)
		classifyWithUndersampling(clf, expX, expY, cheapX, cheapY)
		if gendot:
			generateDotFileWithUndersampling(clf, expX, expY, cheapX, cheapY)
	elif classifier == 'rf':
		clf = ensemble.RandomForestClassifier(max_depth=6)
		classifyWithUndersampling(clf, expX, expY, cheapX, cheapY)

if __name__ == '__main__':
	main()
