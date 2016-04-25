import csv
import numpy as np

def test(csv_path):
    with open(csv_path, 'rb') as fid:
        reader = csv.reader(fid, delimiter='|')
        num_entries = sum(1 for row in reader)
        fid.seek(0)
        print num_entries
        stars_ind = 6
        price_ind = 8
        genre_ind = 9
        score_ind = 10
        stars = []
        prices = []
        genres = []
        scores = []
        reader.next()
        for row in reader:
            stars.append(row[stars_ind])
            prices.append(row[price_ind])
            genres.append(row[genre_ind])
            scores.append(row[score_ind])
        print stars[:3]
        print prices[:3]
        for i in len(genres):
        genres[i] = (genres[i].split
        print genres[:3]
        print scores[:3]

if __name__ == '__main__':
    test('business.csv')
