import json

'''
Prints out all labels and all possible values associated with them
'''

data = []
with open('yelp_dataset_challenge_academic_dataset~/yelp_academic_dataset_review.json') as f:
    for line in f:
        data.append(json.loads(line))

# {
#     'business_id': (encrypted business id),
#     'user_id': (encrypted user id),
#     'stars': (star rating, rounded to half-stars),
#     'text': (review text),
#     'date': (date, formatted like '2012-03-14'),
#     'votes': {(vote type): (count)},
# }

bids = {}

with open('../cleaned_data/bids.txt', 'r') as b:
    for bid in b:
        stripped = bid.rstrip('\n')
        bids[stripped] = ""

with open("../cleaned_data/review.txt", "wb") as r:
    r.write("business_id|stars|date\n")
    for elt in data:
        business_id = elt['business_id'].encode("utf-8")
        stars = elt['stars']
        date = elt['date']
        """
        I'm just taking this part out for now to hopefully fix KeyErrors in business_cleaner_2 --Philip
		if business_id not in bids:
			continue
        """
        toAppend = business_id + "|" + str(stars) + "|" + date + "\n"
        r.write(toAppend)
