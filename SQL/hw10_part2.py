import sqlite3

DB_NAME = 'tweets.sqlite'

try:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
except Error as e:
    print(e)

#prints the tweet with the most number of retweets (just tweet text will do)
def get_most_retweeted_tweet():
    statement = 'SELECT TweetText '
    statement += 'FROM Tweets '
    statement += 'ORDER BY RetweetCount DESC '
    statement += 'LIMIT 1'
    cur.execute(statement)
    for x in cur:
        print(x[0])

#print the user’s screen name who is most followed
def get_most_followed_user():
    statement = 'SELECT ScreenName '
    statement += 'FROM Tweets '
    statement += 'ORDER BY FollowerCount DESC '
    statement += 'LIMIT 1'
    cur.execute(statement)
    for x in cur:
        print(x[0])

#print the user’s screen name who’s tweet had the highest retweet count
def get_most_retweeted_user():
    statement = 'SELECT ScreenName '
    statement += 'FROM Tweets '
    statement += 'ORDER BY RetweetCount DESC '
    statement += 'LIMIT 1'
    cur.execute(statement)
    for x in cur:
        print(x[0])

#print the 5 tweets that belong to authors with highest number of followers. Order this in the the descending order.
def get_tweets_from_most_followed():
    statement = 'SELECT TweetText '
    statement += 'FROM Tweets '
    statement += 'GROUP BY ScreenName '
    statement += 'ORDER BY FollowerCount DESC '
    statement += 'LIMIT 5'
    cur.execute(statement)
    for x in cur:
        print(x[0])

#print the top 5 locations that are tweeting about us/ Going Blue. Order in the descending order.
def get_trending_location():
    statement = 'SELECT Location '
    statement += 'FROM Tweets '
    statement += 'GROUP BY Location '
    statement += 'HAVING TweetText LIKE "%Go Blue%" '
    statement += 'ORDER BY COUNT(*) DESC '
    statement += 'LIMIT 5'
    cur.execute(statement)
    for x in cur:
        print(x[0])

get_most_retweeted_tweet()
get_tweets_from_most_followed()
get_most_followed_user()
get_most_retweeted_user()
get_trending_location()
