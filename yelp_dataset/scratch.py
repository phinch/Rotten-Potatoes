import csv

with open('attributes.txt', 'rb') as fid:
    reader = csv.reader(fid,delimiter='|')
    labels = reader.next()
    firstrow = reader.next()
    print 'num labels:', len(labels)
    print 'num data:', len(firstrow)
    assert len(labels) == len(firstrow)
