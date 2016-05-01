import csv
import random
import sys
import numpy as np
from sklearn import tree
from sklearn import cross_validation

def extractData(datapath):
	with open(datapath, 'rb') as fid:
		reader = csv.reader(fid, delimiter='|')
		labels = reader.next()
		good_inds = [1,2,3,4,5,6,12,14,19,22,25,32,36]
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
				if i==1: # stars
					if curr_val == 'n/a':
						curr_val = 3.0 # average stars
					else:
						curr_val = float(curr_val)
				elif i==6: # noise
					if curr_val in ['loud', 'very_loud']:
						curr_val = 1
					else:
						curr_val = 0
				elif i==14: # attire
					if curr_val in ['formal', 'dressy']:
						curr_val = 1
					else:
						curr_val = 0
				elif i==36: # alcohol
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
	X = [i for i,j in XY]
	Y = [j for i,j in XY]
	return X, Y
		
def main():
	cheapX, cheapY, expX, expY = extractData('attributes_all.txt')
	# create DT classifier
	clf = tree.DecisionTreeClassifier(max_depth = 3)
	num_cheap = len(cheapY)
	num_exp = len(expY)
	print 'Num cheap restaurants:', num_cheap
	print 'Num expensive restaurants:', num_exp
	
	num_iter = 100
	accuracies = []
	
	# Undersample and obtain average score num_iter times, and then average together the average scores
	print 'Undersampling... (will sample/train/test %d cheap and %d expensive %d times)' % (num_exp, num_exp, num_iter)
	sys.stdout.flush()
	for i in range(num_iter):
		cheapXY = random.sample(zip(cheapX, cheapY), num_exp)
		cheapTrainX = [i for i,j in cheapXY]
		cheapTrainY = [j for i,j in cheapXY]
		X = cheapTrainX + expX
		Y = cheapTrainY + expY
		X, Y = shuffleListPairs(X, Y)
		scores = cross_validation.cross_val_score(clf,X,Y,cv=10)
		accuracies.append(scores.mean())
		
	accuracies = np.array(accuracies)
	
	print 'Finished!'
	print 'Accuracy: %0.2f%% (+/- %0.2f%%)' % (accuracies.mean()*100, accuracies.std()*2*100)

		
if __name__ == '__main__':
	main()