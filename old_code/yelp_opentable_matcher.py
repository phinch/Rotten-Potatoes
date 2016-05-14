import math
import csv

f = open('data/opentable_location.txt', 'r')
g = open('data/yelp_providence/yelp_location.txt', 'r')

ot = {}
otr = {}
matchdata = {}

f.readline()
g.readline()

with open('yelp_opentable_matches.txt', 'wb') as h:
	for line in f:
		l = line.split("|")
		restaurant = l[0]
		addrElts = l[1].split(" ")
		addr = addrElts[0] + " " + addrElts[1]
		ot[addr] = restaurant
		otr[restaurant] = addr

	for line in g:
		l = line.split("|")
		restaurant = l[0]
		if l[1] == 'n/a\n':
			continue
		addrElts = l[1].split(" ")
		addr = addrElts[0] + " " + addrElts[1]
		if restaurant in otr:
			print restaurant
		if addr in ot:
			print ot[addr] + " -> " + restaurant
			if ot[addr] == restaurant:
				h.write(restaurant + "\n")
