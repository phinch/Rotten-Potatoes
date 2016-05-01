import csv
from sklearn import tree

#X = [[0,0,1],[0,1,0],[1,0,0],[1,0,0]]
#Y = [0,1,2,4]
#clf = tree.DecisionTreeClassifier()
#clf = clf.fit(X,Y)
#print clf.predict_proba([[1,1,0]])

with open('attributes_one-two.txt', 'rb') as fid:
    reader = csv.reader(fid, delimiter='|')
    labels = reader.next()
    good_inds = [1,2,3,4,5,6,12,13,14,19,22,25,32,36]
    predict_ind = 13
    X = []
    Y = []
    stars = set()
    noise = set()
    price = set()
    attire = set()
    alcohol = set()
    for row in reader:
        feat = []
        for i in good_inds:
            curr_val = row[i]
            if i==6:
				if curr_val in ['loud', 'very_loud']
        X.append(feat)
        Y.append(row[predict_ind])
    print 'stars:', list(stars)
    print 'noise:', list(noise)
    print 'price:', list(price)
    print 'attire:', list(attire)
    print 'alcohol:', list(alcohol)
