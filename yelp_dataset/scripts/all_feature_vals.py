import json
from lxml import html
import requests
import math
import csv

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
#music = {}
with open("../cleaned_data/featlist.txt", "wb") as r:
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
            cnt = True

            if 'Take-out' in attributes:
                takeout = attributes['Take-out']
                if 'Take-out' not in attr:
                    attr['Take-out'] = {}
                    attr['Take-out'][takeout] = 0
                else:
                    attr['Take-out'][takeout] = 0    
            else:
                takeout = na 
            if 'Drive-Thru' in attributes:
                drivethru = attributes['Drive-Thru']
                if 'Drive-Thru' not in attr:
                    attr['Drive-Thru'] = {}
                    attr['Drive-Thru'][drivethru] = 0
                else:
                    attr['Drive-Thru'][drivethru] = 0    
            else:
                drivethru = na
            if 'Outdoor Seating' in attributes:
                outdoorseating = attributes['Outdoor Seating']
                if 'Outdoor Seating' not in attr:
                    attr['Outdoor Seating'] = {}
                    attr['Outdoor Seating'][outdoorseating] = 0
                else:
                    attr['Outdoor Seating'][outdoorseating] = 0    
            else:
                outdoorseating = na
            if 'Caters' in attributes:
                caters = attributes['Caters']
                if 'Caters' not in attr:
                    attr['Caters'] = {}
                    attr['Caters'][caters] = 0
                else:
                    attr['Caters'][caters] = 0    
            else:
                caters = na
            if 'Noise Level' in attributes:
                noise = attributes['Noise Level']
                if 'Noise Level' not in attr:
                    attr['Noise Level'] = {}
                    attr['Noise Level'][noise] = 0
                else:
                    attr['Noise Level'][noise] = 0    
            else:
                noise = na
            if 'Parking' in attributes:
                if 'garage' in attributes['Parking']:
                    p_garage = attributes['Parking']['garage']
                    if 'garage' not in attr:
                        attr['garage'] = {}
                        attr['garage'][p_garage] = 0
                    else:
                        attr['garage'][p_garage] = 0    
                else:
                    p_garage = na
                if 'street' in attributes['Parking']:
                    p_street = attributes['Parking']['street']
                    if 'street' not in attr:
                        attr['street'] = {}
                        attr['street'][p_street] = 0
                    else:
                        attr['street'][p_street] = 0    
                else:
                    p_street = na
                if 'validated' in attributes['Parking']:
                    p_validated = attributes['Parking']['validated']
                    if 'validated' not in attr:
                        attr['validated'] = {}
                        attr['validated'][p_validated] = 0
                    else:
                        attr['validated'][p_validated] = 0   
                else:
                    p_validated = na
                if 'lot' in attributes['Parking']:
                    p_lot = attributes['Parking']['lot']
                    if 'lot' not in attr:
                        attr['lot'] = {}
                        attr['lot'][p_lot] = 0
                    else:
                        attr['lot'][p_lot] = 0   
                else:
                    p_lot = na
                if 'valet' in attributes['Parking']:
                    p_valet = attributes['Parking']['valet']
                    if 'valet' not in attr:
                        attr['valet'] = {}
                        attr['valet'][p_valet] = 0
                    else:
                        attr['valet'][p_valet] = 0   
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
                    attr['delivery'] = {}
                    attr['delivery'][delivery] = 0
                else:
                    attr['delivery'][delivery] = 0   
            else:
                delivery = na
            if 'Price Range' in attributes:
                price = attributes['Price Range']
                if 'price' not in attr:
                    attr['price'] = {}
                    attr['price'][price] = 0
                else:
                    attr['price'][price] = 0  
            else:
                price = na
            if 'Attire' in attributes:
                attire = attributes['Attire']
                if 'attire' not in attr:
                    attr['attire'] = {}
                    attr['attire'][attire] = 0
                else:
                    attr['attire'][attire] = 0  
            else:
                attire = na
            if 'Has TV' in attributes:
                tv = attributes['Has TV']
                if 'tv' not in attr:
                    attr['tv'] = {}
                    attr['tv'][tv] = 0
                else:
                    attr['tv'][tv] = 0  
            else:
                tv = na
            if 'Good For' in attributes:
                if 'dessert' in attributes['Good For']:
                    gf_dessert = attributes['Good For']['dessert']
                    if 'good for dessert' not in attr:
                        attr['good for dessert'] = {}
                        attr['good for dessert'][gf_dessert] = 0
                    else:
                        attr['good for dessert'][gf_dessert] = 0  
                else:
                    gf_dessert = na
                if 'latenight' in attributes['Good For']:
                    gf_latenight = attributes['Good For']['latenight']
                    if 'good for latenight' not in attr:
                        attr['good for latenight'] = {}
                        attr['good for latenight'][gf_latenight] = 0
                    else:
                        attr['good for latenight'][gf_latenight] = 0  
                else:
                    gf_latenight = na
                if 'lunch' in attributes['Good For']:
                    gf_lunch = attributes['Good For']['lunch']
                    if 'good for lunch' not in attr:
                        attr['good for lunch'] = {}
                        attr['good for lunch'][gf_lunch] = 0
                    else:
                        attr['good for lunch'][gf_lunch] = 0  
                else:
                    gf_lunch = na
                if 'dinner' in attributes['Good For']:
                    gf_dinner = attributes['Good For']['dinner']
                    if 'good for dinner' not in attr:
                        attr['good for dinner'] = {}
                        attr['good for dinner'][gf_dinner] = 0
                    else:
                        attr['good for dinner'][gf_dinner] = 0  
                else:
                    gf_dinner = na
                if 'breakfast' in attributes['Good For']:
                    gf_breakfast = attributes['Good For']['breakfast']
                    if 'good for breakfast' not in attr:
                        attr['good for breakfast'] = {}
                        attr['good for breakfast'][gf_breakfast] = 0
                    else:
                        attr['good for breakfast'][gf_breakfast] = 0  
                else:
                    gf_breakfast = na
                if 'brunch' in attributes['Good For']:
                    gf_brunch = attributes['Good For']['brunch']
                    if 'good for brunch' not in attr:
                        attr['good for brunch'] = {}
                        attr['good for brunch'][gf_brunch] = 0
                    else:
                        attr['good for brunch'][gf_brunch] = 0  
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
                    attr['reservations'] = {}
                    attr['reservations'][reservations] = 0
                else:
                    attr['reservations'][reservations] = 0  
            else:
                reservations = na
            if 'Ambience' in attributes:
                if 'romantic' in attributes['Ambience']:
                    a_romantic = attributes['Ambience']['romantic']
                    if 'a_romantic' not in attr:
                        attr['a_romantic'] = {}
                        attr['a_romantic'][a_romantic] = 0
                    else:
                        attr['a_romantic'][a_romantic] = 0  
                else:
                    a_romantic = na
                if 'intimate' in attributes['Ambience']:
                    a_intimate = attributes['Ambience']['intimate']
                    if 'a_intimate' not in attr:
                        attr['a_intimate'] = {}
                        attr['a_intimate'][a_intimate] = 0
                    else:
                        attr['a_intimate'][a_intimate] = 0  
                else:
                    a_intimate = na
                if 'classy' in attributes['Ambience']:
                    a_classy = attributes['Ambience']['classy']
                    # if a_classy:
                    #     count += 1
                    if 'a_classy' not in attr:
                        attr['a_classy'] = {}
                        attr['a_classy'][a_classy] = 0
                    else:
                        attr['a_classy'][a_classy] = 0  
                else:
                    cnt = False
                    a_classy = na
                if  'hipster' in attributes['Ambience']:
                    a_hipster = attributes['Ambience']['hipster']
                    if 'a_hipster' not in attr:
                        attr['a_hipster'] = {}
                        attr['a_hipster'][a_hipster] = 0
                    else:
                        attr['a_hipster'][a_hipster] = 0  
                else:
                    a_hipster = na
                if 'divey' in attributes['Ambience']:
                    a_divey = attributes['Ambience']['divey']
                    if 'a_divey' not in attr:
                        attr['a_divey'] = {}
                        attr['a_divey'][a_divey] = 0
                    else:
                        attr['a_divey'][a_divey] = 0  
                else:
                    a_divey = na
                if 'touristy' in attributes['Ambience']:
                    a_touristy = attributes['Ambience']['touristy']
                    if 'a_touristy' not in attr:
                        attr['a_touristy'] = {}
                        attr['a_touristy'][a_touristy] = 0
                    else:
                        attr['a_touristy'][a_touristy] = 0  
                else:
                    a_touristy = na
                if 'trendy' in attributes['Ambience']:
                    a_trendy = attributes['Ambience']['trendy']
                    if 'a_trendy' not in attr:
                        attr['a_trendy'] = {}
                        attr['a_trendy'][a_trendy] = 0
                    else:
                        attr['a_trendy'][a_trendy] = 0  
                else:
                    a_trendy = na
                if  'upscale' in attributes['Ambience']:
                    a_upscale = attributes['Ambience']['upscale']
                    if 'a_upscale' not in attr:
                        attr['a_upscale'] = {}
                        attr['a_upscale'][a_upscale] = 0
                    else:
                        attr['a_upscale'][a_upscale] = 0  
                else:
                    a_upscale = na
                if 'casual' in attributes['Ambience']:
                    a_casual = attributes['Ambience']['casual']
                    if 'a_casual' not in attr:
                        attr['a_casual'] = {}
                        attr['a_casual'][a_casual] = 0
                    else:
                        attr['a_casual'][a_casual] = 0  
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
                    attr['waiter'] = {}
                    attr['waiter'][waiter] = 0
                else:
                    attr['waiter'][waiter] = 0  
            else:
                waiter = na
            if 'Accepts Credit Cards' in attributes:
                creditcards = attributes['Accepts Credit Cards']
                if 'creditcards' not in attr:
                    attr['creditcards'] = {}
                    attr['creditcards'][creditcards] = 0
                else:
                    attr['creditcards'][creditcards] = 0  
            else:
                creditcards = na
            if 'Good for Kids' in attributes:
                kids = attributes['Good for Kids']
                if 'kids' not in attr:
                    attr['kids'] = {}
                    attr['kids'][kids] = 0
                else:
                    attr['kids'][kids] = 0  
            else:
                kids = na
            if 'Good For Groups' in attributes:
                groups = attributes['Good For Groups']
                if 'groups' not in attr:
                    attr['groups'] = {}
                    attr['groups'][groups] = 0
                else:
                    attr['groups'][groups] = 0  
            else:
                groups = na
            if 'Alcohol' in attributes:
                alcohol = attributes['Alcohol']
                if 'alcohol' not in attr:
                    attr['alcohol'] = {}
                    attr['alcohol'][alcohol] = 0
                else:
                    attr['alcohol'][alcohol] = 0  
            else:
                alcohol = na
            if 'Wheelchair Accessible' in attributes:
                wheelchair = attributes['Wheelchair Accessible']
                if 'wheelchair' not in attr:
                    attr['wheelchair'] = {}
                    attr['wheelchair'][wheelchair] = 0
                else:
                    attr['wheelchair'][wheelchair] = 0  
            else:
                wheelchair = na
            if 'Wi-Fi' in attributes:
                wifi = attributes['Wi-Fi']
                if 'wifi' not in attr:
                    attr['wifi'] = {}
                    attr['wifi'][wifi] = 0
                else:
                    attr['wifi'][wifi] = 0  
            else:
                wifi = na
            if 'Order at Counter' in attributes:
                counter = attributes['Order at Counter']
                if 'counter' not in attr:
                    attr['counter'] = {}
                    attr['counter'][counter] = 0
                else:
                    attr['counter'][counter] = 0  
            else:
                counter = na
            if 'Dogs Allowed' in attributes:
                dogs = attributes['Dogs Allowed']
                if 'dogs' not in attr:
                    attr['dogs'] = {}
                    attr['dogs'][dogs] = 0
                else:
                    attr['dogs'][dogs] = 0  
            else:
                dogs = na
            if 'Good for Dancing' in attributes:
                dancing = attributes['Good for Dancing']
                if 'dancing' not in attr:
                    attr['dancing'] = {}
                    attr['dancing'][dancing] = 0
                else:
                    attr['dancing'][dancing] = 0  
            else:
                dancing = na
            if 'Coat Check' in attributes:
                coat = attributes['Coat Check']
                if 'coat' not in attr:
                    attr['coat'] = {}
                    attr['coat'][coat] = 0
                else:
                    attr['coat'][coat] = 0  
            else:
                coat = na
            if 'Smoking' in attributes:
                smoking = attributes['Smoking']
                if 'smoking' not in attr:
                    attr['smoking'] = {}
                    attr['smoking'][smoking] = 0
                else:
                    attr['smoking'][smoking] = 0  
            else:
                smoking = na
            if 'Happy Hour' in attributes:
                happyhour = attributes['Happy Hour']
                if 'happyhour' not in attr:
                    attr['happyhour'] = {}
                    attr['happyhour'][happyhour] = 0
                else:
                    attr['happyhour'][happyhour] = 0  
            else:
                happyhour = na
            if 'Music' in attributes:
                if 'dj' in attributes['Music']:
                    m_dj = attributes['Music']['dj']
                    if 'm_dj' not in attr:
                        attr['m_dj'] = {}
                        attr['m_dj'][m_dj] = 0
                    else:
                        attr['m_dj'][m_dj] = 0  
                else:
                    m_dj = na
                if 'background_music' in attributes['Music']:
                    m_background = attributes['Music']['background_music']
                    if 'm_background' not in attr:
                        attr['m_background'] = {}
                        attr['m_background'][m_background] = 0
                    else:
                        attr['m_background'][m_background] = 0  
                else:
                    m_background = na
                if 'jukebox' in attributes['Music']:
                    m_jukebox = attributes['Music']['jukebox']
                    if 'm_jukebox' not in attr:
                        attr['m_jukebox'] = {}
                        attr['m_jukebox'][m_jukebox] = 0
                    else:
                        attr['m_jukebox'][m_jukebox] = 0  
                else:
                    m_jukebox = na
                if 'live' in attributes['Music']:
                    m_live = attributes['Music']['live']
                    if 'm_live' not in attr:
                        attr['m_live'] = {}
                        attr['m_live'][m_live] = 0
                    else:
                        attr['m_live'][m_live] = 0  
                else:
                    m_live = na
                if 'video' in attributes['Music']:
                    m_video = attributes['Music']['video']
                    if 'm_video' not in attr:
                        attr['m_video'] = {}
                        attr['m_video'][m_video] = 0
                    else:
                        attr['m_video'][m_video] = 0  
                else:
                    m_video = na
                if 'karaoke' in attributes['Music']:
                    m_karaoke = attributes['Music']['karaoke']
                    if 'm_karaoke' not in attr:
                        attr['m_karaoke'] = {}
                        attr['m_karaoke'][m_karaoke] = 0
                    else:
                        attr['m_karaoke'][m_karaoke] = 0  
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
                    attr['byob'] = {}
                    attr['byob'][byob] = 0
                else:
                    attr['byob'][byob] = 0  
            else:
                byob = na
            if 'Corkage' in attributes:
                corkage = attributes['Corkage']
                if 'corkage' not in attr:
                    attr['corkage'] = {}
                    attr['corkage'][corkage] = 0
                else:
                    attr['corkage'][corkage] = 0  
            else:
                corkage = na
            if 'BYOB/Corkage' in attributes:
                byobcorkage = attributes['BYOB/Corkage']
                if 'byobcorkage' not in attr:
                    attr['byobcorkage'] = {}
                    attr['byobcorkage'][byobcorkage] = 0
                else:
                    attr['byobcorkage'][byobcorkage] = 0  
            else:
                byobcorkage = na
            if 'Open 24 Hours' in attributes:
                tfhours = attributes['Open 24 Hours']
                if 'tfhours' not in attr:
                    attr['tfhours'] = {}
                    attr['tfhours'][tfhours] = 0
                else:
                    attr['tfhours'][tfhours] = 0  
            else:
                tfhours = na
            if 'Ages Allowed' in attributes:
                ages = attributes['Ages Allowed']
                if 'ages' not in attr:
                    attr['ages'] = {}
                    attr['ages'][ages] = 0
                else:
                    attr['ages'][ages] = 0  
            else:
                ages = na
            if 'Dietary Restrictions' in attributes:
                if 'dairy-free' in attributes['Dietary Restrictions']:
                    d_dairyfree = attributes['Dietary Restrictions']['dairy-free']
                    if 'd_dairyfree' not in attr:
                        attr['d_dairyfree'] = {}
                        attr['d_dairyfree'][d_dairyfree] = 0
                    else:
                        attr['d_dairyfree'][d_dairyfree] = 0  
                else:
                    d_dairyfree = na
                if 'gluten-free' in attributes['Dietary Restrictions']:
                    d_glutenfree = attributes['Dietary Restrictions']['gluten-free']
                    if 'd_glutenfree' not in attr:
                        attr['d_glutenfree'] = {}
                        attr['d_glutenfree'][d_glutenfree] = 0
                    else:
                        attr['d_glutenfree'][d_glutenfree] = 0  
                else:
                    d_glutenfree = na
                if 'vegan' in attributes['Dietary Restrictions']:
                    d_vegan = attributes['Dietary Restrictions']['vegan']
                    if 'd_vegan' not in attr:
                        attr['d_vegan'] = {}
                        attr['d_vegan'][d_vegan] = 0
                    else:
                        attr['d_vegan'][d_vegan] = 0  
                else:
                    d_vegan = na
                if 'kosher' in attributes['Dietary Restrictions']:
                    d_kosher = attributes['Dietary Restrictions']['kosher']
                    if 'd_kosher' not in attr:
                        attr['d_kosher'] = {}
                        attr['d_kosher'][d_kosher] = 0
                    else:
                        attr['d_kosher'][d_kosher] = 0  
                else:
                    d_kosher = na
                if 'halal' in attributes['Dietary Restrictions']:
                    d_halal = attributes['Dietary Restrictions']['halal']
                    if 'd_halal' not in attr:
                        attr['d_halal'] = {}
                        attr['d_halal'][d_halal] = 0
                    else:
                        attr['d_halal'][d_halal] = 0  
                else:
                    d_halal = na
                if 'soy-free' in attributes['Dietary Restrictions']:
                    d_soyfree = attributes['Dietary Restrictions']['soy-free']
                    if 'd_soyfree' not in attr:
                        attr['d_soyfree'] = {}
                        attr['d_soyfree'][d_soyfree] = 0
                    else:
                        attr['d_soyfree'][d_soyfree] = 0  
                else:
                    d_soyfree = na
                if 'vegetarian' in attributes['Dietary Restrictions']:
                    d_vegetarian = attributes['Dietary Restrictions']['vegetarian']
                    if 'd_vegetarian' not in attr:
                        attr['d_vegetarian'] = {}
                        attr['d_vegetarian'][d_vegetarian] = 0
                    else:
                        attr['d_vegetarian'][d_vegetarian] = 0  
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
                    attr['appt'] = {}
                    attr['appt'][appt] = 0
                else:
                    attr['appt'][appt] = 0  
            else:
                appt = na
            if 'Accepts Insurance' in attributes:
                insurance = attributes['Accepts Insurance']
                if 'insurance' not in attr:
                    attr['insurance'] = {}
                    attr['insurance'][insurance] = 0
                else:
                    attr['insurance'][insurance] = 0  
            else:
                insurance = na

    for a in attr:
        print str(a) + ": " + str(attr[a])
    # "attributes": 
    # {"Take-out": true, 
    #  "Drive-Thru": false, 
    #  "Outdoor Seating": false, 
    #  "Caters": false, 
    #  "Noise Level": "average", 
    #  "Parking": 
    #     {"garage": false, 
    #      "street": false, 
    #      "validated": false, 
    #      "lot": false, 
    #      "valet": false}, 
    #  "Delivery": false, 
    #  "Price Range": 1, 
    #  "Attire": "casual", 
    #  "Has TV": false, 
    #  "Good For": 
    #     {"dessert": false, 
    #      "latenight": false, 
    #      "lunch": false, 
    #      "dinner": false, 
    #      "breakfast": false, 
    #      "brunch": false}, 
    #  "Takes Reservations": false, 
    #  "Ambience": 
    #     {"romantic": false, 
    #      "intimate": false, 
    #      "classy": false, 
    #      "hipster": false, 
    #      "divey": false, 
    #      "touristy": false, 
    #      "trendy": false, 
    #      "upscale": false, 
    #      "casual": false}, 
    #  "Waiter Service": false, 
    #  "Accepts Credit Cards": true, 
    #  "Good for Kids": true, 
    #  "Good For Groups": true, 
    #  "Alcohol": "none"}
