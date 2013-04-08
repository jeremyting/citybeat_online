from datetime import datetime
from datetime import datetime, timedelta, date
from email.utils import parsedate_tz
from tweet import Tweet
from tweet_interface import TweetInterface
from event import Event
from photo import Photo

import calendar


import operator
import string
import types
import time

class TweetCluster(object):
	
	def __init__(self):
		self._tweet_cluster = {}
		self._tweet_cluster['period'] = None
		self._tweet_cluster['region'] = None
		self._tweet_cluster['tweets'] = []
	
	def setTweetCluster(self, tweet_cluster):
		self._tweet_cluster['tweets'] = tweet_cluster
		
	def setRegion(self, region):
		self._tweet_cluster['region'] = region
		
	def setPeriod(self, period):
		# period should be [begin_time, end time]
		assert period[0] <= period[1]
		self._tweet_cluster['period'] = period
		
	def getNumberOfTweets(self):
		return len(self._tweet_cluster['tweets'])
		
	def getTweetFromRangeQuery(self):
		ti = TweetInterface()
		tweets = ti.rangeQuery(self._tweet_cluster['region'], self._tweet_cluster['period'])
		self._tweet_cluster['tweets'] = []
		for tweet in tweets:
			self._tweet_cluster['tweets'].append(tweet)
			
	def computePercentageOfTweetWithKeyword(self, keywords, k):
		# no tweet
		if len(self._tweet_cluster['tweets']) == 0:
			return 0
		# compute the percentage of tweets with at least k keywords
		occ = 0
		for tweet in self._tweet_cluster['tweets']:
			tweet = Tweet(tweet)
			if tweet.findKeywords(keywords) >= k:
				occ += 1
		return 1.0*occ/len(self._tweet_cluster['tweets'])
		
		
	def getHistoricTweets(self, days=7):
		ti = TweetInterface()
		tweets = []
		for d in xrange(1, days+1):
			et = int(self._tweet_cluster['period'][1]) + 24*3600*d
			bt = int(self._tweet_cluster['period'][0]) + 24*3600*d
			day_tweets = ti.rangeQuery(self._tweet_cluster['region'], [str(bt), str(et)])
			for tweet in day_tweets:
				tweets.append(tweet)
		return tweets
		
	def computeDifferenceComparedWithHistoricPercentageOfTweetWithKeyword(self, keywords, k, days=7):
		if self._tweet_cluster['period'] is None:
			return 0
		freq = self.computePercentageOfTweetWithKeyword(keywords, k)
		tweets = self.getHistoricTweets(days)
		historic_tweet_cluster = TweetCluster()
		historic_tweet_cluster.setTweetCluster(tweets)
		return (self.computePercentageOfTweetWithKeyword(keywords, k) 
		        - historic_tweet_cluster.computePercentageOfTweetWithKeyword(keywords, k))
	
	def makeFakeEvent(self):
		event = {}
		photos = []
		for tweet in self._tweet_cluster['tweets']:
			fake_photo = {}
			fake_photo['caption'] = {}
			fake_photo['caption']['text'] = Tweet(tweet).getRawText()
			fake_photo['user'] = {}
			# user_id of Instagram is string
			fake_photo['user']['id'] = str(tweet['user']['id'])
			photos.append(fake_photo)
		event['photos'] = photos
		return event

	def toJSON(self):
		return self._tweet_cluster	
		
def main():
	ti = TweetInterface()
	period = ['1354910879', '1354918838']
	region = {'min_lat':40.73297324, 'max_lat':40.73827852, 'min_lng':-73.99410076, 'max_lng':-73.98609447999999}
	tc = TwitterCluster()
	tc.setRegion(region)
	tc.setPeriod(period)
	
if __name__ == '__main__':
	main()
		
	