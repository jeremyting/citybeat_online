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
from bson.objectid import ObjectId
from config import InstagramConfig

import config
import time
import logging
import string
import types
import json
import numpy


class TweetInterface(MongoDBInterface):
	
	def __init__(self, db=TwitterConfig.tweet_db,  
	             collection=TwitterConfig.tweet_collection):
	  # initialize an interface for accessing event from mongodb
	  super(TweetInterface, self).__init__()
	  self.setDB(db)
	  self.setCollection(collection)
	  
	def saveDocument(self, tweet):
		if not type(tweet) is types.DictType:
			tweet = tweet.toDict()
		if 'location' not in tweet.keys():
			if 'coordinates' not in tweet.keys():
				return
			if 'coordinates' not in tweet['coordinates'].keys():
				return
			location = {}
			location['latitude'] = tweet['coordinates']['coordinates'][1]
			location['longitude'] = tweet['coordinates']['coordinates'][0]
			tweet['location'] = location
		
		tweet['created_time'] = Tweet(tweet).getCreatedUTCTimestamp()
		
		super(TweetInterface, self).saveDocument(tweet)
	
	def rangeQuery(self, region=None, period=None):
		#period should be specified as: [begin_time end_time]
		#specify begin_time and end_time as the utctimestamp, string!!
		
		if period is not None:
			assert period[0] <= period[1]
		
		region_conditions = {}
		period_conditions = {}
		if not region is None:
		#region should be specified as the class defined in region.py
			if not type(region) is types.DictType:
				region = region.toDict() 
			region_conditions = {'location.latitude':{'$gte':region['min_lat'], '$lte':region['max_lat']},
				                   'location.longitude':{'$gte':region['min_lng'], '$lte':region['max_lng']}
				                   	}
				                   	
		if not period is None:
			period_conditions = {'created_time':{'$gte':str(period[0]), '$lte':str(period[1])}}

		conditions = dict(region_conditions, **period_conditions)
		
		#returns a cursor
		#sort the tweet in chronologically decreasing order
		return self.getAllDocuments(conditions).sort('created_time', -1)


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


def checkTweetInRegion():
	region = {}
	region['min_lat'] = InstagramConfig.photo_min_lat
	region['max_lat'] = InstagramConfig.photo_max_lat
	region['min_lon'] = InstagramConfig.photo_min_lng
	region['max_lon'] = InstagramConfig.photo_max_lng
	
	r = Region(region)
	
	ti = TweetInterface()
	ti.setDB('citybeat')
	ti.setCollection('tweets')
	cur = ti.getAllDocuments()
	tot = 0
	tweet_in_region = 0
	for tweet in cur:
		cor = [0, 0]
		cor[0] = tweet['location']['latitude']
		cor[1] = tweet['location']['latitude']
		tot += 1
		if r.insideRegion(cor):
			tweet_in_region += 1
	
	print tweet_in_region
	print tot
	 
def main():
	
	ti = TweetInterface()
	period = ['1364829908', '1365693908']
	region = {'min_lat':40.73297324, 'max_lat':40.73827852, 'min_lng':-73.99410076, 'max_lng':-73.98609447999999}
	print ti.rangeQuery(region=region, period=period).count()

#	fid = open('nyc_tweets.txt')
#	for line in fid:
#		tweet = json.loads(line.strip())
#		ti.saveDocument(tweet)
#	fid.close()
	
#	ti = TweetInterface()
#	tweet = ti.getDocument()
#	for tweet in tweets:
#		tweet = Tweet(tweet)
##		retweet = tweet.getRetweetFreq()
##		if retweet > 0:
##			print retweet
#		keywords = ['game', 'knicks']
#		if tweet.findKeywords(keywords) == len(keywords):
#			print tweet.getRawText().
#			print 

			
if __name__ == '__main__':
	checkTweetInRegion()
	#transferTweets()
	#getTweetStatistics()
