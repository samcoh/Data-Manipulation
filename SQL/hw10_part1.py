import tweepy
import json
import sys
import sqlite3
from secrets import *

DB_NAME = 'tweets.sqlite'

def get_tweets(search_term, num_tweets):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=search_term).items(num_tweets)]
    return searched_tweets

def init_db(db_name):
    #code to test whether table already exists goes here
    #if exists, prompt to user: "Table exists. Delete?yes/no"
    #if user input is yes, drop table. Else, use move on and use existing table
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        s = 'SELECT COUNT(*) '
        s += 'FROM sqlite_master '
        s += 'WHERE type = "table" AND name ="Tweets"'
        result = cur.execute(s).fetchall()[0][0]
        if result == 1:
            response = input("Tweets Table already exists. Drop table? yes/no: ").lower()
            if response == 'yes':
                # Drop tables: so we can rebuild them from scratch
                statement = '''
                    DROP TABLE IF EXISTS 'Tweets';
                '''
                cur.execute(statement)
                conn.commit()
            else:
                conn.close()
                print("Using Existing Table")
                return
    #handle exception if connection fails by printing the error
    except:
        conn.close()
        print("Error: connection failure")
        return

    #code to create a new database goes here
    #code to create table(if not exists) goes here

    statement = '''
        CREATE TABLE 'Tweets' (
            'TweetId' INTEGER PRIMARY KEY AUTOINCREMENT,
            'TweetText' TEXT NOT NULL,
            'RetweetCount' Integer,
            'UserId' INTEGER NOT NULL,
            'ScreenName' TEXT NOT NULL,
            'Location' TEXT NOT NULL,
            'FollowerCount' INTEGER
        );
    '''
    cur.execute(statement)

    conn.commit()

    #close database connection

    conn.close()

    #this function is not expected to return anything, you can modify this if you want

def insert_tweet_data(tweets):
    #add code to connect to database and get a Cursor
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

    #Uncomment to see our data of interest from the Tweepy Result Set.
    #Comment these print statements when you submit code to us.
    # for tweet in tweets:
    #     print("Tweet ID:", tweet.id)
    #     print("Tweet Text:", tweet.text.encode('utf8'))
    #     print ("Retweet Count:", tweet.retweet_count)
    #     print("User ID:", tweet.user.id)
    #     print("User Screen Name:", tweet.user.screen_name)
    #     print("User Location:", tweet.user.location)
    #     print("User Follower Count:", tweet.user.followers_count)

        #Add code to insert each of these data of interest to the Tweets table
        for tweet in tweets:
            insertion = (None, tweet.text.encode("utf8"),tweet.retweet_count,tweet.user.id,tweet.user.screen_name,tweet.user.location,tweet.user.followers_count)
            statement = 'INSERT INTO Tweets '
            statement += 'VALUES (?,?,?,?,?,?,?)'
            cur.execute(statement, insertion)
            conn.commit()
        conn.close()
    except:
        return "error occured"

    #Close database connection

    #Not expecting return, you can modify if you wish

if __name__ == "__main__":
    search_term = input("Enter search term: ")
    num_tweets = int(input("Enter number of tweets to retrieve: "))
    #fetch tweets
    tweets = get_tweets(search_term, num_tweets)
    print("Fetched",len(tweets),"tweets")
    #create database and table
    init_db(DB_NAME)
    #insert data into table
    insert_tweet_data(tweets)
