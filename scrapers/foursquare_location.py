from lxml import html
import requests
import math
import csv
import json

#put in a number for offset between urlbase and afteroffset, then add all 3 together
urlbase = "https://api.foursquare.com/v2/venues/explore?near=Providence%2C%20RI%2C%20United%20States&nearGeoId=72057594043152087&q=Food&limit=50&offset="
offset = 0
afteroffset = "&client_id=PHXQKJR1W4PZ1PUW2OS2SGOGSGU3DQ0KBAZWM0PFZ2DXC5SE&client_secret=KLXFZC3YYN3N5OL1ZMRJHALA0Z1KXEIKDHLZAJG5XRIACRHJ&v=20140806"

url = urlbase+str(offset)+afteroffset
r = requests.get(url, params={})
results = r.json()["response"]
allfound = "warning" in results

results = results["groups"][0]["items"]

with open("data/foursquare/foursquare.csv", "wb") as r:
    rwriter = csv.writer(r, delimiter = '|')
    rwriter.writerow(["Name", "Price", "Score", "Votes"])

    while(not allfound):
        allfound = True
        for i in range(0, len(results)):
            venue = results[i]["venue"]
            name = venue["name"]
            if "price" in venue:
                price = venue["price"]["tier"]
            else:
                price = "N/A"

            if "rating" in venue:
                score = venue["rating"]
            else:
                continue
            
            if "ratingSignals" in venue:
                votes = venue["ratingSignals"]
            else:
                votes = "N/A"

            rwriter.writerow([name.encode("utf-8"), price, score, votes])

        offset += 50
        url = urlbase+str(offset)+afteroffset
        r = requests.get(url, params={})
        results = r.json()["response"]
        allfound = "warning" in results

        results = results["groups"][0]["items"]
        
