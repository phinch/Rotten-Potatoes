import csv
import sys
import numpy as np
from sklearn.naive_bayes import BernoulliNB
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
						curr_val = 1
					else:
						stars = float(curr_val)
						if stars > 3:
							curr_val = 1
						elif curr_val == 'n/a':
							curr_val = 2
						else:
							curr_val = 0
				elif i == 6:  # noise
					if curr_val in ['loud', 'very_loud']:
						curr_val = 1
					elif curr_val == 'n/a':
						curr_val = 2
					else:
						curr_val = 0
				elif i == 14:  # attire
					if curr_val in ['formal', 'dressy']:
						curr_val = 1
					elif curr_val == 'n/a':
						curr_val = 2
					else:
						curr_val = 0
				elif i == 36:  # alcohol
					if curr_val in ['beer_and_wine', 'full_bar']:
						curr_val = 1
					elif curr_val == 'n/a':
						curr_val = 2
					else:
						curr_val = 0
				else:
					assert curr_val in ['n/a', 'True', 'False']
					if curr_val == 'True':
						curr_val = 1
					elif curr_val == 'n/a':
						curr_val = 2
					else:
						curr_val = 0
				feat.append(curr_val)
			price = row[price_ind]
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
	
def inNestedList(elem, lst):
	return elem in [j for i in lst for j in i]
	
def countInNestedList(elem, lst):
	return sum(j for i in lst for j in i if j==2)
	
def replaceAllTwos(lst):
	newlst = lst[:]
	for i in range(len(lst)):
		for j in range(len(lst[0])):
			curr_val = lst[i][j]
			if curr_val == 2:
				newlst[i][j] = 0
			else:
				newlst[i][j] = curr_val
	return newlst

def main():
	cheapX, cheapY, expX, expY = extractData('../cleaned_data/attributes_all.txt')
	allX = cheapX + expX
	allY = cheapY + expY
	#print inNestedList(2, allX)
	#print countInNestedList(2, allX)
	assert len(allX[0]) == len(cheapX[0]) == len(expX[0])
	numfeat = len(allX[0])
	numall = len(allY)
	assert len(expX[0]) == numfeat
	classifiers = [BernoulliNB() for _ in range(numfeat)]
	# Train classifiers
	print 'Training classifiers...'
	sys.stdout.flush()
	predictable_inds = []
	for i in range(numfeat):
		X = []
		Y = []
		for j in range(numall):
			curr_rest = allX[j]
			currY = curr_rest[i]
			if currY == 2:
				continue
			currX = curr_rest[:i] + curr_rest[i+1:]
			X.append(currX)
			Y.append(currY)
		scores = cross_validation.cross_val_score(classifiers[i], X, Y, cv=5)
		classifiers[i].fit(X, Y)
		acc = scores.mean()
		if acc > 0.7:
			#print '%d\t%f' % (i, acc)
			predictable_inds.append(i)
	print 'Finished!'
	# Predict n/a values
	#print inNestedList(2, allX)
	#print countInNestedList(2, allX)
	print 'Replacing n/as...'
	sys.stdout.flush()
	for i in predictable_inds:
		for j in range(numall):
			curr_rest = allX[j]
			if curr_rest[i] != 2:
				continue
			curr_rest[i] = classifiers[i].predict([curr_rest[:i] + curr_rest[i+1:]])[0]
	allX = replaceAllTwos(allX)
	cheapX = allX[:len(cheapX)]
	expX = allX[len(cheapX):]
	assert len(cheapX) == len(cheapY)
	assert len(expX) == len(expY)
	print 'Finished!'
	print 'Saving arrays...'
	np.save('../cleaned_data/cheapX.npy', np.array(cheapX).astype(int))
	np.save('../cleaned_data/cheapY.npy', np.array(cheapY).astype(int))
	np.save('../cleaned_data/expX.npy', np.array(expX).astype(int))
	np.save('../cleaned_data/expY.npy', np.array(expY).astype(int))
	print 'Finished!'
	#print inNestedList(2, allX)
	#print countInNestedList(2, allX)

if __name__ == '__main__':
	main()
