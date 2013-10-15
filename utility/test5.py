from tweet_interface import TweetInterface
from config import TwitterConfig
from tool import getCurrentStampUTC
import matplotlib.pyplot as plt

def main():
    ti = TweetInterface()

    counts = []
    x = []
    now = 1381536000
    interval = 24*3600
    max = 0
    for day in xrange(3000):
        begin_time = now - (day + 1) * interval
        end_time = now - day * interval
        c = ti.rangeQuery(period=[begin_time, end_time], fields='_id').count()
        counts.append(c)
        x.append(str((12-day)%30))
        if c > 0:
            if c > max:
                max = c
        print max
'''
    plt.plot(range(len(counts)), counts)
    plt.xticks(range(len(counts)), x)
    plt.xlabel('Date from 10/12/2013 to 09/13/2013')
    plt.ylabel('Number of tweets in Mongodb')
    plt.title('Number of tweets during the past 30 days')
    plt.show()
'''

def testWithExtendedTweets():
    ti = TweetInterface(collection=TwitterConfig.extended_tweet_collection)
    tweets = {}
    most_popular_tweet = ''
    max_retweet_count = -1
    for tweet in ti.getAllFields(fields='text'):
        text = tweet['text']
        count = tweets.get(text, 0)
        count += 1
        tweets[text] = count
        if count > max_retweet_count:
            max_retweet_count = count
            most_popular_tweet = text

    print most_popular_tweet, max_retweet_count
    print len(tweets)

testWithExtendedTweets()
import re
twitter_username_re = re.compile(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)')
mentions = twitter_username_re.findall('fsdg @fucasg @sdfg!! 154@163.com @xia!!')
print mentions