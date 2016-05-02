import csv
import numpy as np
from sklearn import linear_model,linear_model,datasets
import matplotlib.pyplot as plt

def extract_data(csv_path):
    with open(csv_path, 'rb') as fid:
        reader = csv.reader(fid, delimiter='|')
        state_ind = 3
        price_ind = 8
        genre_ind = 9
        score_ind = 10
        states = []
        prices = []
        genres = []
        scores = []
        reader.next()
        for row in reader:
            states.append(row[state_ind])
            prices.append(row[price_ind])
            genres.append(row[genre_ind])
            scores.append(row[score_ind])
        prices = [int(i) if i != 'N/A' else None for i in prices]
        scores = [float(i) if i != 'N/A' else None for i in scores]
        genres = [tuple(g.strip() for g in i.split('///')) for i in genres]

        # if a list contains None at an index, remove that index from all other lists.
        len_data = len(scores)
        assert(len(states) == len(prices) == len(genres) == len_data)
        for i in range(len_data):
            if prices[i] is None or scores[i] is None:
                states[i] = prices[i] = genres[i] = scores[i] = None
        states = [s for s in states if s is not None]
        prices = [p for p in prices if p is not None]
        genres = [g for g in genres if g is not None]
        scores = [s for s in scores if s is not None]

        data = dict()
        data['states'] = states
        data['prices'] = prices
        data['genres'] = genres
        data['scores'] = scores
        return data

def iris_test(): # example code for LogisticRegression
    iris = datasets.load_iris()
    X = iris.data[:,:2] # first two features
    Y = iris.target
    h=.02 # step size in the mesh
    logreg = linear_model.LogisticRegression()
    logreg.fit(X,Y)

    x_min, x_max = X[:,0].min() - .5, X[:,0].max() + .5
    y_min, y_max = X[:,1].min() - .5, X[:,1].max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = logreg.predict(np.c_[xx.ravel(), yy.ravel()])

    Z = Z.reshape(xx.shape)
    plt.figure(1, figsize=(4,3))
    plt.pcolormesh(xx,yy,Z,cmap=plt.cm.Paired)

    plt.scatter(X[:,0],X[:,1],c=Y,edgecolors='k',cmap=plt.cm.Paired)
    plt.xlabel('Sepal length')
    plt.ylabel('Sepal width')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.show()

def process_data(data):
    prices = data['prices']
    scores = data['scores']
    prices = [[i] for i in prices]
    len_data = len(prices)
    test_size = int(len_data*0.2)
    Xtrain = prices[:-test_size]
    Xtest = prices[-test_size:]
    Ytrain = scores[:-test_size]
    Ytest = scores[-test_size:]

    regr = linear_model.LinearRegression()
    regr.fit(Xtrain,Ytrain)
    print 'Coefficients: \n', regr.coef_
    print 'Residual sum of squares: %.2f' % np.mean((regr.predict(Xtest)-Ytest)**2)
    print 'Variance score: %.2f' % regr.score(Xtest,Ytest)

    plt.scatter(Xtest,Ytest,color='black')
    plt.plot(Xtest,regr.predict(Xtest),color='blue',linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.show()

def main():
    data = extract_data('../cleaned_data/business.csv')
    states = data['states']
    prices = data['prices']
    genres = data['genres']
    scores = data['scores']
    assert(None not in states and None not in prices and None not in genres and None not in scores)
    assert(len(states) == len(prices) == len(genres) == len(scores))
    process_data(data)

if __name__ == '__main__':
    main()
    #iris_test()
