## proj_nps.py
## Skeleton for Project 2, Winter 2018
## ~~~ modify this file, but don't rename it ~~~
import requests
import json
from bs4 import BeautifulSoup
import sys
from requests_oauthlib import OAuth1
import secrets

#CACHING:
try:
    cache_file = open('cache_sites.json', 'r')
    cache_contents = cache_file.read()
    CACHE_SITES= json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_SITES = {}
try:
    cache_file_nearby = open('cache_nearby.json', 'r')
    cache_contents_nearby = cache_file_nearby.read()
    CACHE_NEARBY = json.loads(cache_contents_nearby)
    cache_file_nearby.close()
except:
    CACHE_NEARBY = {}

try:
    cache_file_tweets = open('cache_tweets.json', 'r')
    cache_contents_tweets = cache_file_tweets.read()
    CACHE_TWEETS = json.loads(cache_contents_tweets)
    cache_file_tweets.close()
except:
    CACHE_TWEETS = {}
def get_unique_key(url):
  return url
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)
def make_request_using_cache_sites(baseurl):
    unique_ident = get_unique_key(baseurl)
    if unique_ident in CACHE_SITES:
      return CACHE_SITES[unique_ident]
    else:
      resp = requests.get(baseurl)
      CACHE_SITES[unique_ident] = resp.text
      dumped_json_cache = json.dumps(CACHE_SITES)
      fw = open('cache_sites.json',"w")
      fw.write(dumped_json_cache)
      fw.close()
      return CACHE_SITES[unique_ident]
def make_request_using_cache(baseurl, params):
    key = params_unique_combination(baseurl, params)
    if key in CACHE_NEARBY:
        return CACHE_NEARBY[key]
    else:
        resp = requests.get(baseurl, params)
        r = json.loads(resp.text)
        CACHE_NEARBY[key] = r
        dumped_json_cache = json.dumps(CACHE_NEARBY)
        fw = open('cache_nearby.json',"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_NEARBY[key]
def make_request_using_cache_twitter(baseurl, params, auth):
    key = params_unique_combination(baseurl, params)
    if key in CACHE_TWEETS:
        return CACHE_TWEETS[key]
    else:
        resp = requests.get(baseurl, params, auth= auth)
        r = json.loads(resp.text)['statuses']
        CACHE_TWEETS[key] = r
        dumped_json_cache = json.dumps(CACHE_TWEETS)
        fw = open('cache_tweets.json',"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_TWEETS[key]

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NationalSite:
    def __init__(self, type = "No Type", name= "No Name", desc= "No Description", url = None, street="No Street", city= "No City", state= "No State", zip_code="No Zip Code"):
        self.type = type
        self.name = name
        self.description = desc
        self.url = url

        self.address_street = street
        self.address_city = city
        self.address_state = state
        self.address_zip = zip_code
    def __str__(self):
        return "{} ({}): {}, {}, {} {}".format(self.name, self.type, self.address_street, self.address_city, self.address_state,self.address_zip)

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
    def __init__(self, name= "No Name", lat = "No Latitude", lng= "No Longitude"):
        self.name = name
        self.lat = lat
        self.lng = lng
    def __str__(self):
        return self.name

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class Tweet:
    def __init__(self, text = "No Text", username = "No username", creation_date = "No creation date", num_retweets = "No retweets", num_favorites = " No favorites", popularity_score = "No Popularity Score", ID= "No Id"):
        self.text = text
        self.username = username
        self.creation_date = creation_date
        self.num_retweets = num_retweets
        self.num_favorites = num_favorites
        self.popularity_score = popularity_score
        self.ID = ID
    def __str__(self):
        return '@'+ self.username+': '+self.text + '\n' + "[retweeted "+str(self.num_retweets)+' times]\n' + "[favorited "+str(self.num_favorites)+' times]\n' + "[popularity: "+str(self.popularity_score)+']\n' + "[tweeted on "+ str(self.creation_date) + "]"+ " | [id: "+ str(self.ID) + ']'

## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov
def get_sites_for_state(state_abbr):
    baseurl = 'https://www.nps.gov/state/{}/index.htm'.format(state_abbr)
    page_text= make_request_using_cache_sites(baseurl)
    #page_text = requests.get(baseurl).text
    page_soup = BeautifulSoup(page_text, 'html.parser')
    #get type, name, description, url
    content = page_soup.find_all('div', class_= 'col-md-9 col-sm-9 col-xs-12 table-cell list_left')
    base = 'https://www.nps.gov'
    list_parks = []
    for x in content:
        type_park = x.find("h2").text

        name = x.find('a').text

        descrip_park = x.find('p').text.strip()

        second_half = x.find('a')['href']
        url = base + second_half

        page_text = make_request_using_cache_sites(url)
        page_soup =  BeautifulSoup(page_text, 'html.parser')
        address_data = page_soup.find_all('p', class_= 'adr')
        if len(address_data) == 0:
            park = NationalSite(type = type_park, name = name, desc = descrip_park, url = url)
            list_parks.append(park)
        for y in address_data:
            try:
                street_with_br = y.find('span', itemprop = "streetAddress",class_= 'street-address')
                for x in street_with_br.find_all('br'):
                  x.replace_with(", ")
                street1 = street_with_br.text.strip()
                lstreet = street1.split()
                street = ' '.join(lstreet)

                #street = y.find('span', itemprop = "streetAddress",class_= 'street-address').text.strip()
            except:
                street = "No Street"
            try:
                city = y.find('span', itemprop="addressLocality").text.strip()
            except:
                city = "No City"
            try:
                state = y.find('span', itemprop="addressRegion",class_="region").text.strip()
            except:
                state = "No State"
            try:
                zip_code = y.find('span',itemprop="postalCode", class_="postal-code").text.strip()
            except:
                zip_code = "No Zip Code"
            park = NationalSite(type = type_park, name = name, desc = descrip_park, url = url, street = street, city = city, state = state, zip_code = zip_code)
            list_parks.append(park)
    return list_parks

# list_ = get_sites_for_state('ca')
# print(list_[0].address_street)

## Must return the list of NearbyPlaces for the specified NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list
def get_nearby_places_for_site(site_object):
    name = site_object.name
    type_ = site_object.type
    name_type = name +" "+type_
    baseurl_text_search= 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    params = {'key': secrets.google_places_key,'query': name_type}
    info = make_request_using_cache(baseurl_text_search, params)
    if len(info['results'])== 0:
        return []
    lat_lng_dict = info['results'][0]['geometry']['location']
    latitude = lat_lng_dict['lat']
    longitude = lat_lng_dict['lng']
    lat_and_lng= str(latitude)+','+str(longitude)

    baseurl_nearby_search = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    params_for_nearby = {'key': secrets.google_places_key, 'location': lat_and_lng,'radius': '10000'}
    info_nearby = make_request_using_cache(baseurl_nearby_search, params_for_nearby)

    if len(info_nearby['results']) == 0:
        return []
    results = info_nearby['results']
    list_of_nearby_places = []
    for x in results:
        name = x['name']
        lat,lng = x['geometry']['location']['lat'],x['geometry']['location']['lng']

        instance = NearbyPlace(name, lat, lng)
        list_of_nearby_places.append(instance)
    return list_of_nearby_places
# parks = get_sites_for_state("az")
# first_object = parks[0]
# print(get_nearby_places_for_site(first_object))
# site1 = NationalSite('National Monument','Sunset Crater Volcano', 'A volcano in a crater.')
# print(get_nearby_places_for_site(site1))


## Must return the list of Tweets that mention the specified NationalSite
## param: a NationalSite object
## returns: a list of up to 10 Tweets, in descending order of "popularity"
def get_tweets_for_site(site_object):
    consumer_key = secrets.twitter_api_key
    consumer_secret = secrets.twitter_api_secret
    access_token = secrets.twitter_access_token
    access_secret = secrets.twitter_access_token_secret

    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
    requests.get(url, auth = auth)

    twitter_url = 'https://api.twitter.com/1.1/search/tweets.json?'
    name = site_object.name
    type_= site_object.type
    full_name = name +" "+ type_
    params = {'q': full_name, 'count': 100,'lang': 'en', 'result_type': 'mixed'}
    info = make_request_using_cache_twitter(twitter_url, params, auth)
    tweet_info = []
    num = 0
    if len(info) == 0:
        return []
    for x in info:
        if "RT" not in x["text"].split()[0]:
            num = num + 1
            if num > 10:
                break
            text = x['text'].strip()
            username = x['user']['screen_name'].strip()
            creation_date = x["created_at"]
            num_retweets = x["retweet_count"]
            num_favorites = x["favorite_count"]
            popularity_score = (num_retweets * 2) + (num_favorites * 3)
            ID = x['id']
            instance = Tweet(text = text, username = username, creation_date = creation_date, num_retweets = num_retweets, num_favorites = num_favorites, popularity_score = popularity_score, ID = ID)
            tweet_info.append(instance)
    sort_tweet_info = sorted(tweet_info, key = lambda x: x.popularity_score, reverse = True)
    return sort_tweet_info
#site1 = NationalSite('National Monument','Sunset Crater Volcano', 'A volcano in a crater.')
#print(get_tweets_for_site(site1))
#site2 = get_sites_for_state('il')
#print(get_tweets_for_site(site2[0]))

if __name__ == '__main__':
    user = input("Enter command (or 'help' for options): ")
    while user != "exit":
        user = user.split()
        states = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
            }
        num = 0
        if user[0] == "list":
            try:
              full_name = "state name"
              for abbrev in states:
                  if user[1].upper() == abbrev:
                      full_name = states[abbrev]
              print("National Sites in {}: ".format(full_name))
              parks = get_sites_for_state(user[1])
              parks_dic_num = {}
              for x in parks:
                  num = num + 1
                  parks_dic_num[num] = x
                  print(str(num)+'. '+ x.__str__())
              num = 0
            except:
              user = input("Please enter a valid command (or help for options): ")
              if user == "exit":
                print("Goodbye!")
                break
              else:
                continue
        elif user[0] == 'nearby':
            try:
              if int(user[1]) not in list(parks_dic_num.keys()):
                  print("You entered an invalid number from the list of National Sites.")
                  user = input("Please re-enter the nearby command ('nearby' valid number), or select a different command: ")
                  if user == "exit":
                    print("Goodbye!")
                  continue
              nearby_dic_num = {}
              for x in parks_dic_num:
                  if str(x) == user[1]:
                      national_park = parks_dic_num[x]
                      places_near = get_nearby_places_for_site(national_park)
              if len(places_near) > 0:
                  print("Places near "+ national_park.name +" "+ national_park.type)
                  for L in places_near:
                      num = num + 1
                      nearby_dic_num[num] = L
                      print(str(num)+". "+L.name)
              else:
                  print("I'm sorry, we are unable to find the places nearby" )
                  user = input("Please re-enter the nearby command ('nearby' valid number), or select a different command: ")
                  if user == "exit":
                    print("Goodbye!")
                  continue
              num = 0
            except:
              user = input("Please enter a valid command (or help for options): ")
              if user == "exit":
                print("Goodbye!")
                break
              else:
                continue
        elif user[0] == 'tweets':
            try:
              keys = list(parks_dic_num.keys())
              if int(user[1]) not in keys:
                  print("You entered an invalid number from the list of National Sites.")
                  user = input("Please re-enter the nearby command ('tweets' valid number), or select a different command: ")
                  if user == "exit":
                    print("Goodbye!")
                  continue
              for x in parks_dic_num:
                  if str(x) == user[1]:
                      national_park_tweets = parks_dic_num[x]
                      tweets_parks = get_tweets_for_site(national_park_tweets)
              if len(tweets_parks) == 0:
                  print("I'm sorry, we were unable to find recent tweets for the park you selected.")
                  user = input("Please re-enter the tweets command ('tweets' number), or select a different command: ")
                  if user == "exit":
                    print("Goodbye!")
                  continue
              for x in tweets_parks:
                  print(x)
                  print("-"*20)
            except:
              user = input("Please enter a valid command (or help for options): ")
              if user == "exit":
                print("Goodbye!")
                break
              else:
                continue
        elif user[0] == 'help':
            print("\tlist <stateabbr>")
            print("\t \tavailable anytime")
            print("\t \tlists all National Sites in a state")
            print("\t \tvalid inputs: a two-letter state abbreviation")

            print("\tnearby <result_number>")
            print("\t \tavailable only if there is an active result set")
            print("\t \tlists all Places nearby a given result")
            print("\t \tvalid inputs: an integer 1-len (result_set_size)")

            print("\ttweets <result_number>")
            print("\t \tavailable only if there is an active results set")
            print("\t \tlists up to 10 most 'popular' tweets that mention the selected Site")

            print("\texit")
            print("\t \texits the program")

            print("\thelp")
            print("\t \tlists available commands (these instructions)")
        else:
            user = input("Please enter a valid command (or help for options): ")
            if user == "exit":
              print("Goodbye!")
              break
            else:
              continue
        user = input("Enter command (or 'help' for options): ")
        if user == "exit":
          print('Goodbye!')
