import datetime
import tweepy
from tweepy.error import TweepError
#from tweepy.parsers import RawJsonParser
import json
import time
import sys

import pymongo

def tweepy_auth():
    CONSUMER_KEY = '01gugiESt8CSq97ypjTQg'
    CONSUMER_SECRET = 'JQPPGBxZploR3fG9TDylDH3ZrjJgcHlsLSR5SSBY'
    ACCESS_KEY = '3183721-QQZ4rpf5cv3og207hSwHFPGpsTf5v7kPuY6MO9S9iY'
    ACCESS_SECRET = '2DP9FW6ZmCis4TewZLYHQGbqWiThq4uQqSQbJSiFJw'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    #api = tweepy.API(auth)
    return auth


#tweepy parser
import tweepy
import json
 
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
             
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, db_name):
        tweepy.StreamListener.__init__(self)
        self.mid_list = []
        self.db_name = db_name
    def save_to_mongo(self,tweet):
        tweet = json.loads(tweet.json)
        if tweet['coordinates'] is None:
            return
        mongo = pymongo.Connection("grande.rutgers.edu",27017)
        mongo_db = mongo[self.db_name]
        mongo_collection = mongo_db.tweets
        #find closest mid point as mid_lat, mid_lng
        tweet['_id'] = tweet['id']
        mongo_collection.save(tweet)

    def on_status(self, status):
        try:
            #print "%s\t%s\t%s\t%s\t%s" % (status.text, 
            #        status.author.screen_name, 
            #        status.created_at, 
            #        status.source,
            #        status.coordinates['coordinates']
            #        )
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
    auth = tweepy_auth()
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener('tweets'), timeout=60)
    streaming_api.filter(follow=None, locations=[-74.0547045, 40.696614,-73.8700515,40.813458])
           

if __name__=="__main__":
    main()

