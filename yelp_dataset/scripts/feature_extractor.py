import json
from lxml import html
import requests
import math
import csv

'''
Writes restaurants and their features in the 1-2 $ price tier to a csv file
'''

# JSON format
# {
#     'type': 'business',
#     'business_id': (encrypted business id),
#     'name': (business name),
#     'neighborhoods': [(hood names)],
#     'full_address': (localized address),
#     'city': (city),
#     'state': (state),
#     'latitude': latitude,
#     'longitude': longitude,
#     'stars': (star rating, rounded to half-stars),
#     'review_count': review count,
#     'categories': [(localized category names)]
#     'open': True / False (corresponds to closed, not business hours),
#     'hours': {
#         (day_of_week): {
#             'open': (HH:MM),
#             'close': (HH:MM)
#         },
#         ...
#     },
#     'attributes': {
#         (attribute_name): (attribute_value),
#         ...
#     },
# }

# attr = {}
#music = {}
with open("../cleaned_data/attributes_one-two.txt", "wb") as r:
    r.write("business_id|stars|takeout|drivethru|outdoorseating|caters|noise|p_garage|p_street|p_validated|p_lot|p_valet|delivery|price|attire|tv|gf_dessert|gf_latenight|gf_lunch|gf_dinner|gf_breakfast|gf_brunch|reservations|a_romantic|a_intimate|a_classy|a_hipster|a_divey|a_touristy|a_trendy|a_upscale|a_casual|waiter|creditcards|kids|groups|alcohol|wheelchair|wifi|counter|dogs|dancing|coat|smoking|happyhour|m_dj|m_background|m_jukebox|m_live|m_video|m_karaoke|byob|corkage|byobcorkage|tfhours|ages|d_dairyfree|d_glutenfree|d_vegan|d_kosher|d_halal|d_soyfree|d_vegetarian|appt|insurance\n")

    with open('../data/restaurants.json') as f:
        for line in f:
            elt = json.loads(line)
            business_id = elt['business_id'].encode("utf-8")
            stars = elt['stars']
            attributes = elt['attributes']

            # for a in attributes:
            #     if a not in attr:
            #         attr[a] = 0
            #         print a
            # for a in attributes:
            #     if a == "Music":
            #         for b in attributes["Music"]:
            #             if b not in music:
            #                 music[b] = 0
            #                 print b
            na = "n/a"
            cnt = False

            if 'Take-out' in attributes:
                takeout = attributes['Take-out']
            else:
                takeout = na 
            if 'Drive-Thru' in attributes:
                drivethru = attributes['Drive-Thru']
            else:
                drivethru = na
            if 'Outdoor Seating' in attributes:
                outdoorseating = attributes['Outdoor Seating']
            else:
                outdoorseating = na
            if 'Caters' in attributes:
                caters = attributes['Caters']
            else:
                caters = na
            if 'Noise Level' in attributes:
                noise = attributes['Noise Level']
            else:
                noise = na
            if 'Parking' in attributes:
                if 'garage' in attributes['Parking']:
                    p_garage = attributes['Parking']['garage']
                else:
                    p_garage = na
                if 'street' in attributes['Parking']:
                    p_street = attributes['Parking']['street']
                else:
                    p_street = na
                if 'validated' in attributes['Parking']:
                    p_validated = attributes['Parking']['validated']
                else:
                    p_validated = na
                if 'lot' in attributes['Parking']:
                    p_lot = attributes['Parking']['lot']
                else:
                    p_lot = na
                if 'valet' in attributes['Parking']:
                    p_valet = attributes['Parking']['valet']
                else:
                    p_valet = na
            else:
                p_garage = na
                p_street = na
                p_validated = na
                p_lot = na
                p_valet = na
            if 'Delivery' in attributes:
                delivery = attributes['Delivery']
            else:
                delivery = na
            if 'Price Range' in attributes:
                price = attributes['Price Range']
                if price == 3:
                    cnt = True
                if price == 4:
                    cnt = True
            else:
                price = na
                cnt = True
            if 'Attire' in attributes:
                attire = attributes['Attire']
            else:
                attire = na
            if 'Has TV' in attributes:
                tv = attributes['Has TV']
            else:
                tv = na
            if 'Good For' in attributes:
                if 'dessert' in attributes['Good For']:
                    gf_dessert = attributes['Good For']['dessert']
                else:
                    gf_dessert = na
                if 'latenight' in attributes['Good For']:
                    gf_latenight = attributes['Good For']['latenight']
                else:
                    gf_latenight = na
                if 'lunch' in attributes['Good For']:
                    gf_lunch = attributes['Good For']['lunch']
                else:
                    gf_lunch = na
                if 'dinner' in attributes['Good For']:
                    gf_dinner = attributes['Good For']['dinner']
                else:
                    gf_dinner = na
                if 'breakfast' in attributes['Good For']:
                    gf_breakfast = attributes['Good For']['breakfast']
                else:
                    gf_breakfast = na
                if 'brunch' in attributes['Good For']:
                    gf_brunch = attributes['Good For']['brunch']
                else:
                    gf_brunch = na
            else:
                gf_dessert = na
                gf_latenight = na
                gf_lunch = na
                gf_dinner = na
                gf_breakfast = na
                gf_brunch = na
            if 'Takes Reservations' in attributes:
                reservations = attributes['Takes Reservations']
            else:
                reservations = na
            if 'Ambience' in attributes:
                if 'romantic' in attributes['Ambience']:
                    a_romantic = attributes['Ambience']['romantic']
                else:
                    a_romantic = na
                if 'intimate' in attributes['Ambience']:
                    a_intimate = attributes['Ambience']['intimate']
                else:
                    a_intimate = na
                if 'classy' in attributes['Ambience']:
                    a_classy = attributes['Ambience']['classy']
                    # count += 1
                else:
                    cnt = True
                    a_classy = na
                if  'hipster' in attributes['Ambience']:
                    a_hipster = attributes['Ambience']['hipster']
                else:
                    a_hipster = na
                if 'divey' in attributes['Ambience']:
                    a_divey = attributes['Ambience']['divey']
                else:
                    a_divey = na
                if 'touristy' in attributes['Ambience']:
                    a_touristy = attributes['Ambience']['touristy']
                else:
                    a_touristy = na
                if 'trendy' in attributes['Ambience']:
                    a_trendy = attributes['Ambience']['trendy']
                else:
                    a_trendy = na
                if  'upscale' in attributes['Ambience']:
                    a_upscale = attributes['Ambience']['upscale']
                else:
                    a_upscale = na
                if 'casual' in attributes['Ambience']:
                    a_casual = attributes['Ambience']['casual']
                else:
                    a_casual = na
            else:
                a_romantic = na
                a_intimate = na
                a_classy = na
                a_hipster = na
                a_divey = na
                a_touristy = na
                a_trendy = na
                a_upscale = na
                a_casual = na
                cnt = True
            if 'Waiter Service' in attributes:
                waiter = attributes['Waiter Service']
            else:
                waiter = na
            if 'Accepts Credit Cards' in attributes:
                creditcards = attributes['Accepts Credit Cards']
            else:
                creditcards = na
            if 'Good for Kids' in attributes:
                kids = attributes['Good for Kids']
            else:
                kids = na
            if 'Good For Groups' in attributes:
                groups = attributes['Good For Groups']
            else:
                groups = na
            if 'Alcohol' in attributes:
                alcohol = attributes['Alcohol']
            else:
                alcohol = na
            if 'Wheelchair Accessible' in attributes:
                wheelchair = attributes['Wheelchair Accessible']
            else:
                wheelchair = na
            if 'Wi-Fi' in attributes:
                wifi = attributes['Wi-Fi']
            else:
                wifi = na
            if 'Order at Counter' in attributes:
                counter = attributes['Order at Counter']
            else:
                counter = na
            if 'Dogs Allowed' in attributes:
                dogs = attributes['Dogs Allowed']
            else:
                dogs = na
            if 'Good for Dancing' in attributes:
                dancing = attributes['Good for Dancing']
            else:
                dancing = na
            if 'Coat Check' in attributes:
                coat = attributes['Coat Check']
            else:
                coat = na
            if 'Smoking' in attributes:
                smoking = attributes['Smoking']
            else:
                smoking = na
            if 'Happy Hour' in attributes:
                happyhour = attributes['Happy Hour']
            else:
                happyhour = na
            if 'Music' in attributes:
                if 'dj' in attributes['Music']:
                    m_dj = attributes['Music']['dj']
                else:
                    m_dj = na
                if 'background_music' in attributes['Music']:
                    m_background = attributes['Music']['background_music']
                else:
                    m_background = na
                if 'jukebox' in attributes['Music']:
                    m_jukebox = attributes['Music']['jukebox']
                else:
                    m_jukebox = na
                if 'live' in attributes['Music']:
                    m_live = attributes['Music']['live']
                else:
                    m_live = na
                if 'video' in attributes['Music']:
                    m_video = attributes['Music']['video']
                else:
                    m_video = na
                if 'karaoke' in attributes['Music']:
                    m_karaoke = attributes['Music']['karaoke']
                else:
                    m_karaoke = na
            else:
                m_dj = na
                m_background = na
                m_jukebox = na
                m_live = na
                m_video = na
                m_karaoke = na
            if 'BYOB' in attributes:
                byob = attributes['BYOB']
            else:
                byob = na
            if 'Corkage' in attributes:
                corkage = attributes['Corkage']
            else:
                corkage = na
            if 'BYOB/Corkage' in attributes:
                byobcorkage = attributes['BYOB/Corkage']
            else:
                byobcorkage = na
            if 'Open 24 Hours' in attributes:
                tfhours = attributes['Open 24 Hours']
            else:
                tfhours = na
            if 'Ages Allowed' in attributes:
                ages = attributes['Ages Allowed']
            else:
                ages = na
            if 'Dietary Restrictions' in attributes:
                if 'dairy-free' in attributes['Dietary Restrictions']:
                    d_dairyfree = attributes['Dietary Restrictions']['dairy-free']
                else:
                    d_dairyfree = na
                if 'gluten-free' in attributes['Dietary Restrictions']:
                    d_glutenfree = attributes['Dietary Restrictions']['gluten-free']
                else:
                    d_glutenfree = na
                if 'vegan' in attributes['Dietary Restrictions']:
                    d_vegan = attributes['Dietary Restrictions']['vegan']
                else:
                    d_vegan = na
                if 'kosher' in attributes['Dietary Restrictions']:
                    d_kosher = attributes['Dietary Restrictions']['kosher']
                else:
                    d_kosher = na
                if 'halal' in attributes['Dietary Restrictions']:
                    d_halal = attributes['Dietary Restrictions']['halal']
                else:
                    d_halal = na
                if 'soy-free' in attributes['Dietary Restrictions']:
                    d_soyfree = attributes['Dietary Restrictions']['soy-free']
                else:
                    d_soyfree = na
                if 'vegetarian' in attributes['Dietary Restrictions']:
                    d_vegetarian = attributes['Dietary Restrictions']['vegetarian']
                else:
                    d_vegetarian = na
            else:
                d_dairyfree = na
                d_glutenfree = na
                d_vegan = na
                d_kosher = na
                d_halal = na
                d_soyfree = na
                d_vegetarian = na
            if 'By Appointment Only' in attributes:
                appt = attributes['By Appointment Only']
            else:
                appt = na
            if 'Accepts Insurance' in attributes:
                insurance = attributes['Accepts Insurance']
            else:
                insurance = na

            if not cnt:
                toAppend = business_id + "|" + str(stars) + "|" + str(takeout) + "|" + str(drivethru) + "|" + str(outdoorseating) + "|" + str(caters) + "|" + str(noise) + "|" + str(p_garage) + "|" + str(p_street) + "|" + str(p_validated) + "|" + str(p_lot) + "|" + str(p_valet) + "|" + str(delivery) + "|" + str(price) + "|" + str(attire) + "|" + str(tv) + "|" + str(gf_dessert) + "|" + str(gf_latenight) + "|" + str(gf_lunch) + "|" + str(gf_dinner) + "|" + str(gf_breakfast) + "|" + str(gf_brunch) + "|" + str(reservations) + "|" + str(a_romantic) + "|" + str(a_intimate) + "|" + str(a_classy) + "|" + str(a_hipster) + "|" + str(a_divey) + "|" + str(a_touristy) + "|" + str(a_trendy) + "|" + str(a_upscale) + "|" + str(a_casual) + "|" + str(waiter) + "|" + str(creditcards) + "|" + str(kids) + "|" + str(groups) + "|" + str(alcohol) + "|" + str(wheelchair) + "|" + str(wifi) + "|" + str(counter) + "|" + str(dogs) + "|" + str(dancing) + "|" + str(coat) + "|" + str(smoking) + "|" + str(happyhour) + "|" + str(m_dj) + "|" + str(m_background) + "|" + str(m_jukebox) + "|" + str(m_live) + "|" + str(m_video) + "|" + str(m_karaoke) + "|" + str(byob) + "|" + str(corkage) + "|" + str(byobcorkage) + "|" + str(tfhours) + "|" + str(ages) + "|" + str(d_dairyfree) + "|" + str(d_glutenfree) + "|" + str(d_vegan) + "|" + str(d_kosher) + "|" + str(d_halal) + "|" + str(d_soyfree) + "|" + str(d_vegetarian) + "|" + str(appt) + "|" + str(insurance) + "\n"
                r.write(toAppend)
    print count1
    print count2
    print count3
    print count4