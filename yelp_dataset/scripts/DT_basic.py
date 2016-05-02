import csv
from sklearn import tree
from sklearn import cross_validation

def extractData(datapath):
	with open(datapath, 'rb') as fid:
		reader = csv.reader(fid, delimiter='|')
		labels = reader.next()
		good_inds = [1,2,3,4,5,6,12,14,19,22,25,32,36]
		price_ind = 13
		X = []
		Y = []
		for row in reader:
			if row[price_ind] == 'n/a':
				continue
			feat = []
			for i in good_inds:
				curr_val = row[i]
				if i==1: # stars
					if curr_val == 'n/a':
						curr_val = 3.5 # average
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
			X.append(feat)
			Y.append(price)

	return X,Y


def generateDotFile(clf,X,Y):
	clf = clf.fit(X,Y)
	with open('../dt_graphic_representation/DT_basic.dot', 'w') as f:
		f = tree.export_graphviz(clf, out_file=f)
		
if __name__ == '__main__':
	X,Y = extractData('../cleaned_data/attributes_all.txt')
	assert len(X) == len(Y)
	clf = tree.DecisionTreeClassifier(max_depth = 3)
	scores = cross_validation.cross_val_score(clf,X,Y,cv=10)
	print 'Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std()*2)
