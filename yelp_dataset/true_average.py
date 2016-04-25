"""
Just prints out the true average. Used as a constant in the viz

"""
from lxml import html
import requests
import math
import csv
import json

scores = {} #Name of genre, [yscore, ycount]

biz_reader = csv.reader(open('business.txt', 'rb'), delimiter = "|")
next(biz_reader, None)

score = 0
count = 0

for line in biz_reader: 
    mycount = int(line[7])
    if line[10] == "N/A":
        continue
    myscore = float(line[10])*mycount

    score += myscore
    count += mycount

print (score/count)

