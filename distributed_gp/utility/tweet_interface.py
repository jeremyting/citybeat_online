##########
# Author: Chaolun Xia, 2013-Jan-09#
#
# A high level interface to access the alarm data, for labeling the event
##########
#Edited by: (Please write your name here)#

from mongodb_interface import MongoDBInterface
from tweet import Tweet
from config import TwitterConfig
from datetime import datetime
from element_interface import ElementInterface

import config
import time
import string
import types
import json
import numpy


class TweetInterface(ElementInterface):
    
    def __init__(self, db=TwitterConfig.tweet_db,  
                 collection=TwitterConfig.tweet_collection):
      # initialize an interface for accessing tweet from mongodb
      super(TweetInterface, self).__init__(db, collection, 'tweets')

    def saveDocument(self, tweet):
        if not type(tweet) is types.DictType:
            tweet = tweet.toDict()
        if 'location' not in tweet.keys():
            if 'coordinates' not in tweet.keys():
                return False
            if 'coordinates' not in tweet['coordinates'].keys():
                return False
            location = {}
            location['latitude'] = tweet['coordinates']['coordinates'][1]
            location['longitude'] = tweet['coordinates']['coordinates'][0]
            tweet['location'] = location
            
            if (location['latitude'] < TwitterConfig.min_lat or location['latitude'] > TwitterConfig.max_lat
                    or location['longitude'] < TwitterConfig.min_lng or location['longitude'] > TwitterConfig.max_lng):
                return False
        
        tweet['created_time'] = Tweet(tweet).getCreatedUTCTimestamp()
        
        super(TweetInterface, self).saveDocument(tweet)
        return True

def getTweetStatistics():
    ti = TweetInterface()
    ti.setDB('citybeat_production')
    ti.setCollection('tweets')
    cur = ti.getAllDocuments()
    
    lats = []
    lons = []
    for tweet in cur:
        lat = tweet['location']['latitude']
        lon = tweet['location']['longitude']
        lats.append(lat)
        lons.append(lon)
        
    print [numpy.min(lats), numpy.max(lats), numpy.std(lats),
                 numpy.mean(lats), numpy.median(lats)]
    
    print '*********************************'
    
    print [numpy.min(lons), numpy.max(lons), numpy.std(lons),
                 numpy.mean(lons), numpy.median(lons)]  
    
    
def findEarliestTweet():
    ti = TweetInterface()
    ti.setDB('citybeat_production')
    ti.setCollection('tweets')
    cur = ti.getAllDocuments()
    created_time = '2364829908'
    for tweet in cur:
        if tweet['created_time'] < created_time:
            created_time = tweet['created_time']
    print created_time

def readTweets():
    ti = TweetInterface()
    ti.setDB('tweets')
    ti.setCollection('tweets_from_socialflow')
    cur = ti.getAllDocuments()
    fid = open('/.freespace/citybeat_tweets/nyc_all_tweets')
    suc = 0
    fail = 0
    i = 0
    for line in fid:
        tweet = json.loads(line)
        tweet['_id'] = tweet['id_str']
        res = ti.saveDocument(tweet)
        if res:
            suc += 1
        else:
            fail += 1
        i += 1
        if i % 100 == 0:
            print suc, fail
    fid.close()

def transferTweets():
    ti = TweetInterface()
    ti.setDB('tweets')
    ti.setCollection('tweets')
    cur = ti.getAllDocuments()
    
    ti2 = TweetInterface()
    ti2.setDB('citybeat_production')
    ti2.setCollection('tweets')
    ids = set()
    for tweet in cur:
        id = tweet['id_str']
        if id in ids:
            continue
        ids.add(id)
        tweet['_id'] = id
        ti2.saveDocument(tweet)

def getTweetDistribution():
    ti = TweetInterface()
    ti.setDB('citybeat_production')
    ti.setCollection('tweets')
    cur = ti.getAllFields('created_time')
    earliest = 2363910281
    latest = 363910281
    histagram = {}
    for tuple in cur:
        time = int(tuple['created_time'])
        if time > latest:
            latest = time
        if time < earliest:
            earliest = time
        hour = time / (3600*24)
        histagram[hour] = histagram.get(hour, 0) + 1

    res = []
    for key, value in histagram.items():
        res.append((key, value))

    sorted(res, key=itemgetter(1))

    for key, value in res:
        print key, value

def testWithTweet():
    ti = TweetInterface()
    cur = ti.getAllDocuments()
    for t in cur:
        print len(Tweet(t).getText().strip())


if __name__ == '__main__':
    getTweetDistribution()
