import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import datetime
import tweepy
from tweepy.error import TweepError
import json
import time
import sys
from utility.tweet_interface import TweetInterface
from utility.config import TwitterConfig
#tweepy parser
import tweepy
import json
import pymongo

def tweepy_auth():
    CONSUMER_KEY = 'bkjREJaBNXJIlAG7x9g'
    CONSUMER_SECRET = 'IJCCqMAErMIb5dyzrkPBmnqiPcOvg1wxoz3zB3A7I'
    ACCESS_KEY = '925570813-L5Ek1ZDE2V5spfBMhB11RdK8Lz9Tk2uWed74rRIw'
    ACCESS_SECRET = 'Ek4sjwW4a0BXXi2w4jJrf1gtoYrhhNIRdBgXr9RtU'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return auth

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, db=TwitterConfig.tweet_db, collection=TwitterConfig.tweet_collection):
        tweepy.StreamListener.__init__(self)
        self.mid_list = []
        self.ti = TweetInterface(db=db, collection=collection)

    def save_to_mongo(self,tweet):
        tweet = json.loads(tweet.json)
        tweet['_id'] = tweet['id']
        print type(tweet)
        self.ti.saveDocument(tweet, must_have_geo_tag=False)

    def on_status(self, status):
        print 'get'
        try:
            print "%s\t%s\t%s\t%s" % (status.text,
                    status.author.screen_name,
                    status.created_at,
                    status.source,
                    )
            self.save_to_mongo(status)
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass
        def on_error(self, status_code):
            print >> sys.stderr, 'Encountered error with status code:', status_code
            return True # Don't kill the stream
        def on_timeout(self):
            print >> sys.stderr, 'Timeout...'
            return True # Don't kill the stream

def main():
    print 'in'
    auth = tweepy_auth()
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(collection='extended_tweets'), timeout=60)
    terms = ['ny', 'nyc', 'new york', 'new york city']
    streaming_api.filter(track=terms)

if __name__=="__main__":
    main()
