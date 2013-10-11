import random

from event_interface import EventInterface
from tweet_interface import TweetInterface
from photo_interface import PhotoInterface
from tweet import Tweet
from photo import Photo
from photo_event import PhotoEvent



def main():
    ti = TweetInterface()
    ti.setDB('citybeat_production')
    ti.setCollection('tweets')
    tc = ti.getAllDocuments({'created_time' : {'$gte' : '1378711668'}})
    print tc.count()
    cnt = 0
    for tweet in tc:
        tweet = Tweet(tweet)
        text = tweet.getText().lower()
        if 'quinn' in text:
            print text
            cnt += 1
    print cnt

def test():
    ei = EventInterface(collection='instagram_front_end_events')
    cur = ei.getAllDocuments(limit=2)
    for e in cur:
        e = PhotoEvent(e)
        print e.getID()
        print e.getAllPhotoImageUrls()

if __name__ == '__main__':
    #main()
    test()
