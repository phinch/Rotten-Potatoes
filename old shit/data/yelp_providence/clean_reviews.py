#!/usr/bin/env python
import sys
import csv
import operator

def main():   
    f = open('reviews.txt', 'r')
    g = open('clean_reviews.txt', 'wb')

    curStr = ""
    cleanStr = []

    for line in f:
        pipeCount = 0
        curStr += line
        for letter in curStr:
            if letter == '|':
                pipeCount += 1
        if pipeCount == 6:
            cs = curStr.replace("\n", "")
            cleanStr.append(cs)
            curStr = ""

    for cs in cleanStr:
        g.write(cs + '\n')

if __name__ == '__main__':
    main()
