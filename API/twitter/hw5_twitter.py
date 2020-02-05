from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time: section 003 , 9:00-10:30
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
#this is setting up OAuth session, going to use this as a parameter in requests.get (you can use requests.get in this homework)
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret) #you are going to pass that into your requests.get function
requests.get(url, auth = auth)
#Code for OAuth ends

#Write your code below:

#Code for Part 3: Caching
CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r') #try to open and read contents
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents) #assign contents to a dictionary
    cache_file.close()
# if there was no file, no worries (the above failed). There will be soon! Assign cache_diction to an empty dictionary
except:
    CACHE_DICTION = {}

# A helper function that accepts 2 parameters (set the keys that you will use in your cache)
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
##creates a unique key for accessing different calls made in the cache

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)


# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)
#key to access the data that is returned
def make_request_using_cache(baseurl, params):
    key = params_unique_combination(baseurl, params)
    if key in CACHE_DICTION:
        print("fetching cached data...")
        return CACHE_DICTION[key]
    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, params, auth = auth)
        r = json.loads(resp.text)
        CACHE_DICTION[key] = r #add response to cache dictionary
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w") #opening up the file
        fw.write(dumped_json_cache) #and writing it into there
        fw.close() # Close the open file
        return CACHE_DICTION[key]



#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweets
twitter_url= 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params = {'screen_name': 'umsi', 'count': 25}
# r= requests.get(twitter_url, params=params, auth=auth)
# json_load= json.loads(r.text)
# f= open('tweet.json', 'w')
# f.write(json.dumps(json_load, indent=4))
# f.close
#
# tweets_1=[]
# for x in json_load:
#     tweets_1.append(x['text'])
# big_string="".join(tweets_1)
# print(tweets_1)
cache = make_request_using_cache(twitter_url, params)
tweets =[]
for x in cache:
    tweets.append(x['text'])
big_string = ''.join(tweets)

#Code for Part 2:Analyze Tweets

#creates a list of tokens

tokens = nltk.word_tokenize(big_string)
#Creates frequency distribution from list
#Notice how you can incorporate conditional statements here

freqDist = nltk.FreqDist(token for token in tokens if token.isalpha() and "http" and 'https' and 'RT' not in token)
for word, frequency in freqDist.most_common(5): #looping through the words with the most common frequencies
    print(word + " " + str(frequency))



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
