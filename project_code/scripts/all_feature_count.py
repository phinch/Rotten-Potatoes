import json
from lxml import html
import requests
import math
import csv

'''
Prints out all labels and the number of restaurants whose JSON object contains that label
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

attr = {}
count = 0

with open("../cleaned_data/featlist.txt", "wb") as r:
    # iterate through each restaurant JSON
    with open('../data/restaurants.json') as f:
        for line in f:
            elt = json.loads(line)
            business_id = elt['business_id'].encode("utf-8")
            stars = elt['stars']
            attributes = elt['attributes']

            na = "n/a"
            cnt = True

            if 'Take-out' in attributes:
                takeout = attributes['Take-out']
                if 'Take-out' not in attr:
                    attr['Take-out'] = 1
                else:
                    attr['Take-out'] = attr['Take-out'] + 1    
            else:
                takeout = na 
            if 'Drive-Thru' in attributes:
                drivethru = attributes['Drive-Thru']
                if 'Drive-Thru' not in attr:
                    attr['Drive-Thru'] = 1
                else:
                    attr['Drive-Thru'] = attr['Drive-Thru'] + 1  
            else:
                drivethru = na
            if 'Outdoor Seating' in attributes:
                outdoorseating = attributes['Outdoor Seating']
                if 'Outdoor Seating' not in attr:
                    attr['Outdoor Seating'] = 1
                else:
                    attr['Outdoor Seating'] = attr['Outdoor Seating'] + 1    
            else:
                outdoorseating = na
            if 'Caters' in attributes:
                caters = attributes['Caters']
                if 'Caters' not in attr:
                    attr['Caters'] = 1
                else:
                    attr['Caters'] = attr['Caters'] + 1
            else:
                caters = na
            if 'Noise Level' in attributes:
                noise = attributes['Noise Level']
                if 'Noise Level' not in attr:
                    attr['Noise Level'] = 1
                else:
                    attr['Noise Level'] = attr['Noise Level'] + 1    
            else:
                noise = na
            if 'Parking' in attributes:
                if 'garage' in attributes['Parking']:
                    p_garage = attributes['Parking']['garage']
                    if 'garage' not in attr:
                        attr['garage'] = 1
                    else:
                        attr['garage'] = attr['garage'] + 1    
                else:
                    p_garage = na
                if 'street' in attributes['Parking']:
                    p_street = attributes['Parking']['street']
                    if 'street' not in attr:
                        attr['street'] = 1
                    else:
                        attr['street'] = attr['street']    
                else:
                    p_street = na
                if 'validated' in attributes['Parking']:
                    p_validated = attributes['Parking']['validated']
                    if 'validated' not in attr:
                        attr['validated'] = 1
                    else:
                        attr['validated'] = attr['validated'] + 1   
                else:
                    p_validated = na
                if 'lot' in attributes['Parking']:
                    p_lot = attributes['Parking']['lot']
                    if 'lot' not in attr:
                        attr['lot'] = 1
                    else:
                        attr['lot'] = attr['lot'] + 1
                else:
                    p_lot = na
                if 'valet' in attributes['Parking']:
                    p_valet = attributes['Parking']['valet']
                    if 'valet' not in attr:
                        attr['valet'] = 1
                    else:
                        attr['valet']= attr['valet'] + 1
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
                if 'delivery' not in attr:
                    attr['delivery'] = 1
                else:
                    attr['delivery'] = attr['delivery'] + 1
            else:
                delivery = na
            if 'Price Range' in attributes:
                price = attributes['Price Range']
                if 'price' not in attr:
                    attr['price'] = 1
                else:
                    attr['price'] = attr['price'] + 1
            else:
                price = na
            if 'Attire' in attributes:
                attire = attributes['Attire']
                if 'attire' not in attr:
                    attr['attire'] = 1
                else:
                    attr['attire'] = attr['attire'] + 1
            else:
                attire = na
            if 'Has TV' in attributes:
                tv = attributes['Has TV']
                if 'tv' not in attr:
                    attr['tv'] = 1
                else:
                    attr['tv'] = attr['tv'] + 1
            else:
                tv = na
            if 'Good For' in attributes:
                if 'dessert' in attributes['Good For']:
                    gf_dessert = attributes['Good For']['dessert']
                    if 'good for dessert' not in attr:
                        attr['good for dessert'] = 1
                    else:
                        attr['good for dessert'] = attr['good for dessert'] + 1 
                else:
                    gf_dessert = na
                if 'latenight' in attributes['Good For']:
                    gf_latenight = attributes['Good For']['latenight']
                    if 'good for latenight' not in attr:
                        attr['good for latenight'] = 1
                    else:
                        attr['good for latenight'] = attr['good for latenight'] + 1  
                else:
                    gf_latenight = na
                if 'lunch' in attributes['Good For']:
                    gf_lunch = attributes['Good For']['lunch']
                    if 'good for lunch' not in attr:
                        attr['good for lunch'] = 1
                    else:
                        attr['good for lunch'] = attr['good for lunch'] + 1
                else:
                    gf_lunch = na
                if 'dinner' in attributes['Good For']:
                    gf_dinner = attributes['Good For']['dinner']
                    if 'good for dinner' not in attr:
                        attr['good for dinner'] = 1
                    else:
                        attr['good for dinner'] = attr['good for dinner'] + 1  
                else:
                    gf_dinner = na
                if 'breakfast' in attributes['Good For']:
                    gf_breakfast = attributes['Good For']['breakfast']
                    if 'good for breakfast' not in attr:
                        attr['good for breakfast'] = 1
                    else:
                        attr['good for breakfast'] = attr['good for breakfast'] + 1
                else:
                    gf_breakfast = na
                if 'brunch' in attributes['Good For']:
                    gf_brunch = attributes['Good For']['brunch']
                    if 'good for brunch' not in attr:
                        attr['good for brunch'] = 1
                    else:
                        attr['good for brunch'] = attr['good for brunch'] + 1 
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
                if 'reservations' not in attr:
                    attr['reservations'] = 1
                else:
                    attr['reservations'] = attr['reservations'] + 1 
            else:
                reservations = na
            if 'Ambience' in attributes:
                if 'romantic' in attributes['Ambience']:
                    a_romantic = attributes['Ambience']['romantic']
                    if 'a_romantic' not in attr:
                        attr['a_romantic'] = 1
                    else:
                        attr['a_romantic'] = attr['a_romantic'] + 1
                else:
                    a_romantic = na
                if 'intimate' in attributes['Ambience']:
                    a_intimate = attributes['Ambience']['intimate']
                    if 'a_intimate' not in attr:
                        attr['a_intimate'] = 1
                    else:
                        attr['a_intimate'] = attr['a_intimate'] + 1
                else:
                    a_intimate = na
                if 'classy' in attributes['Ambience']:
                    a_classy = attributes['Ambience']['classy']
                    if 'a_classy' not in attr:
                        attr['a_classy'] = 1
                    else:
                        attr['a_classy'] = attr['a_classy'] + 1
                else:
                    cnt = False
                    a_classy = na
                if  'hipster' in attributes['Ambience']:
                    a_hipster = attributes['Ambience']['hipster']
                    if 'a_hipster' not in attr:
                        attr['a_hipster'] = 1
                    else:
                        attr['a_hipster'] = attr['a_hipster'] + 1
                else:
                    a_hipster = na
                if 'divey' in attributes['Ambience']:
                    a_divey = attributes['Ambience']['divey']
                    if 'a_divey' not in attr:
                        attr['a_divey'] = 1
                    else:
                        attr['a_divey'] = attr['a_divey'] + 1
                else:
                    a_divey = na
                if 'touristy' in attributes['Ambience']:
                    a_touristy = attributes['Ambience']['touristy']
                    if 'a_touristy' not in attr:
                        attr['a_touristy'] = 1
                    else:
                        attr['a_touristy'] = attr['a_touristy'] + 1
                else:
                    a_touristy = na
                if 'trendy' in attributes['Ambience']:
                    a_trendy = attributes['Ambience']['trendy']
                    if 'a_trendy' not in attr:
                        attr['a_trendy'] = 1
                    else:
                        attr['a_trendy'] = attr['a_trendy'] + 1 
                else:
                    a_trendy = na
                if  'upscale' in attributes['Ambience']:
                    a_upscale = attributes['Ambience']['upscale']
                    if 'a_upscale' not in attr:
                        attr['a_upscale'] = 1
                    else:
                        attr['a_upscale'] = attr['a_upscale'] + 1
                else:
                    a_upscale = na
                if 'casual' in attributes['Ambience']:
                    a_casual = attributes['Ambience']['casual']
                    if 'a_casual' not in attr:
                        attr['a_casual'] = 1
                    else:
                        attr['a_casual'] = attr['a_casual'] + 1 
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
                cnt = False
            if 'Waiter Service' in attributes:
                waiter = attributes['Waiter Service']
                if 'waiter' not in attr:
                    attr['waiter'] = 1
                else:
                    attr['waiter'] = attr['waiter'] + 1
            else:
                waiter = na
            if 'Accepts Credit Cards' in attributes:
                creditcards = attributes['Accepts Credit Cards']
                if 'creditcards' not in attr:
                    attr['creditcards'] = 1
                else:
                    attr['creditcards'] = attr['creditcards'] + 1 
            else:
                creditcards = na
            if 'Good for Kids' in attributes:
                kids = attributes['Good for Kids']
                if 'kids' not in attr:
                    attr['kids'] = 1
                else:
                    attr['kids'] = attr['kids'] + 1
            else:
                kids = na
            if 'Good For Groups' in attributes:
                groups = attributes['Good For Groups']
                if 'groups' not in attr:
                    attr['groups'] = 1
                else:
                    attr['groups'] = attr['groups'] + 1
            else:
                groups = na
            if 'Alcohol' in attributes:
                alcohol = attributes['Alcohol']
                if 'alcohol' not in attr:
                    attr['alcohol'] = 1
                else:
                    attr['alcohol'] = attr['alcohol'] + 1 
            else:
                alcohol = na
            if 'Wheelchair Accessible' in attributes:
                wheelchair = attributes['Wheelchair Accessible']
                if 'wheelchair' not in attr:
                    attr['wheelchair'] = 1
                else:
                    attr['wheelchair'] = attr['wheelchair'] + 1
            else:
                wheelchair = na
            if 'Wi-Fi' in attributes:
                wifi = attributes['Wi-Fi']
                if 'wifi' not in attr:
                    attr['wifi'] = 1
                else:
                    attr['wifi'] = attr['wifi'] + 1 
            else:
                wifi = na
            if 'Order at Counter' in attributes:
                counter = attributes['Order at Counter']
                if 'counter' not in attr:
                    attr['counter'] = 1
                else:
                    attr['counter'] = attr['counter'] + 1 
            else:
                counter = na
            if 'Dogs Allowed' in attributes:
                dogs = attributes['Dogs Allowed']
                if 'dogs' not in attr:
                    attr['dogs'] = 1
                else:
                    attr['dogs'] = attr['dogs'] + 1 
            else:
                dogs = na
            if 'Good for Dancing' in attributes:
                dancing = attributes['Good for Dancing']
                if 'dancing' not in attr:
                    attr['dancing'] = 1
                else:
                    attr['dancing'] = attr['dancing'] + 1 
            else:
                dancing = na
            if 'Coat Check' in attributes:
                coat = attributes['Coat Check']
                if 'coat' not in attr:
                    attr['coat'] = 1
                else:
                    attr['coat'] = attr['coat'] + 1
            else:
                coat = na
            if 'Smoking' in attributes:
                smoking = attributes['Smoking']
                if 'smoking' not in attr:
                    attr['smoking'] = 1
                else:
                    attr['smoking'] = attr['smoking'] + 1
            else:
                smoking = na
            if 'Happy Hour' in attributes:
                happyhour = attributes['Happy Hour']
                if 'happyhour' not in attr:
                    attr['happyhour'] = 1
                else:
                    attr['happyhour'] = attr['happyhour'] + 1  
            else:
                happyhour = na
            if 'Music' in attributes:
                if 'dj' in attributes['Music']:
                    m_dj = attributes['Music']['dj']
                    if 'm_dj' not in attr:
                        attr['m_dj'] = 1
                    else:
                        attr['m_dj'] = attr['m_dj'] + 1 
                else:
                    m_dj = na
                if 'background_music' in attributes['Music']:
                    m_background = attributes['Music']['background_music']
                    if 'm_background' not in attr:
                        attr['m_background'] = 1
                    else:
                        attr['m_background'] = attr['m_background'] + 1
                else:
                    m_background = na
                if 'jukebox' in attributes['Music']:
                    m_jukebox = attributes['Music']['jukebox']
                    if 'm_jukebox' not in attr:
                        attr['m_jukebox'] = 1
                    else:
                        attr['m_jukebox'] = attr['m_jukebox'] + 1
                else:
                    m_jukebox = na
                if 'live' in attributes['Music']:
                    m_live = attributes['Music']['live']
                    if 'm_live' not in attr:
                        attr['m_live'] = 1
                    else:
                        attr['m_live'] = attr['m_live'] + 1 
                else:
                    m_live = na
                if 'video' in attributes['Music']:
                    m_video = attributes['Music']['video']
                    if 'm_video' not in attr:
                        attr['m_video'] = 1
                    else:
                        attr['m_video'] = attr['m_video'] + 1
                else:
                    m_video = na
                if 'karaoke' in attributes['Music']:
                    m_karaoke = attributes['Music']['karaoke']
                    if 'm_karaoke' not in attr:
                        attr['m_karaoke'] = 1
                    else:
                        attr['m_karaoke'] = attr['m_karaoke'] + 1
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
                if 'byob' not in attr:
                    attr['byob'] = 1
                else:
                    attr['byob'] = attr['byob'] + 1 
            else:
                byob = na
            if 'Corkage' in attributes:
                corkage = attributes['Corkage']
                if 'corkage' not in attr:
                    attr['corkage'] = 1
                else:
                    attr['corkage'] = attr['corkage'] + 1  
            else:
                corkage = na
            if 'BYOB/Corkage' in attributes:
                byobcorkage = attributes['BYOB/Corkage']
                if 'byobcorkage' not in attr:
                    attr['byobcorkage'] = 1
                else:
                    attr['byobcorkage'] = attr['byobcorkage'] + 1 
            else:
                byobcorkage = na
            if 'Open 24 Hours' in attributes:
                tfhours = attributes['Open 24 Hours']
                if 'tfhours' not in attr:
                    attr['tfhours'] = 1
                else:
                    attr['tfhours'] = attr['tfhours'] + 1
            else:
                tfhours = na
            if 'Ages Allowed' in attributes:
                ages = attributes['Ages Allowed']
                if 'ages' not in attr:
                    attr['ages'] = 1
                else:
                    attr['ages'] = attr['ages'] + 1
            else:
                ages = na
            if 'Dietary Restrictions' in attributes:
                if 'dairy-free' in attributes['Dietary Restrictions']:
                    d_dairyfree = attributes['Dietary Restrictions']['dairy-free']
                    if 'd_dairyfree' not in attr:
                        attr['d_dairyfree'] = 1
                    else:
                        attr['d_dairyfree'] = attr['d_dairyfree'] + 1
                else:
                    d_dairyfree = na
                if 'gluten-free' in attributes['Dietary Restrictions']:
                    d_glutenfree = attributes['Dietary Restrictions']['gluten-free']
                    if 'd_glutenfree' not in attr:
                        attr['d_glutenfree'] = 1
                    else:
                        attr['d_glutenfree'] = attr['d_glutenfree'] + 1
                else:
                    d_glutenfree = na
                if 'vegan' in attributes['Dietary Restrictions']:
                    d_vegan = attributes['Dietary Restrictions']['vegan']
                    if 'd_vegan' not in attr:
                        attr['d_vegan'] = 1
                    else:
                        attr['d_vegan'] = attr['d_vegan'] + 1
                else:
                    d_vegan = na
                if 'kosher' in attributes['Dietary Restrictions']:
                    d_kosher = attributes['Dietary Restrictions']['kosher']
                    if 'd_kosher' not in attr:
                        attr['d_kosher'] = 1
                    else:
                        attr['d_kosher'] = attr['d_kosher'] + 1
                else:
                    d_kosher = na
                if 'halal' in attributes['Dietary Restrictions']:
                    d_halal = attributes['Dietary Restrictions']['halal']
                    if 'd_halal' not in attr:
                        attr['d_halal'] = 1
                    else:
                        attr['d_halal'] = attr['d_halal'] + 1
                else:
                    d_halal = na
                if 'soy-free' in attributes['Dietary Restrictions']:
                    d_soyfree = attributes['Dietary Restrictions']['soy-free']
                    if 'd_soyfree' not in attr:
                        attr['d_soyfree'] = 1
                    else:
                        attr['d_soyfree'] = attr['d_soyfree'] + 1
                else:
                    d_soyfree = na
                if 'vegetarian' in attributes['Dietary Restrictions']:
                    d_vegetarian = attributes['Dietary Restrictions']['vegetarian']
                    if 'd_vegetarian' not in attr:
                        attr['d_vegetarian'] = 1
                    else:
                        attr['d_vegetarian'] = attr['d_vegetarian'] + 1
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
                if 'appt' not in attr:
                    attr['appt'] = 1
                else:
                    attr['appt'] = attr['appt'] + 1
            else:
                appt = na
            if 'Accepts Insurance' in attributes:
                insurance = attributes['Accepts Insurance']
                if 'insurance' not in attr:
                    attr['insurance'] = 1
                else:
                    attr['insurance'] = attr['insurance'] + 1
            else:
                insurance = na

    for a in attr:
        print str(a) + ": " + str(attr[a])

