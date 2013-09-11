import random

from event_interface import EventInterface
from tweet_interface import TweetInterface
from photo_interface import PhotoInterface
from tweet import Tweet
from photo import Photo



def main():
    ti = TweetInterface()
    ti.setDB('citybeat_production')
    ti.setCollection('tweets')
    tc = ti.getAllDocuments({'created_time' : {'&gte' : '1378711668'}})
    print tc.count()
    cnt = 0
    for tweet in tc:
        tweet = Tweet(tweet)
        text = tweet.getText()
        if 'Quinn4NY ' in text:
            cnt += 1
    print cnt

def test():
    pi = PhotoInterface()
    pi.setDB('citybeat_production')
    pi.setCollection('photos')
    cur = pi.getAllDocuments()
    print cur.count()
    cnt = 0
    for photo in cur:
        photo = Photo(photo)
        if 'Quinn4NY' in photo.getText():
            cnt += 1
    print cnt

if __name__ == '__main__':
    main()
    test()
