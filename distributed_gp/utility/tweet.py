from datetime import datetime

from email.utils import parsedate_tz, mktime_tz


import operator
import string
import types
import time


class Tweet(object):
	
	def __init__(self, tweet=None):
		# the input argument event should be a json, dictionary
		if not tweet is None:
			if type(tweet) is types.DictType:
				self._tweet = tweet
			else:
				print tweet
				self._tweet = tweet.toDict() 
	
	def getCreatedUTCTimestamp(self):
		ts = self._tweet['created_at']
		dt = int(mktime_tz(parsedate_tz(ts.strip())))
		return str(dt)
	
	def toDict(self):
		# return a dict, not json
		return self._tweet
		
	def getLocations(self):
		lat = float(self._tweet['location']['latitude'])
		lon = float(self._tweet['location']['longitude'])
		return [lat, lon]
		
	def getRawText(self):
		return self._tweet['text'].strip().lower()
		
	def findKeywords(self, keywords):
		text = self.getRawText()
		occur = 0
		for word in keywords:
			if word in text:
				occur += 1
		return occur
	
	def getRetweetFreq(self):
		return int(self._tweet['retweet_count'])
		
def main():
	ts = 'Fri Dec 07 16:12:48 +0800 2012'
	dt = int(mktime_tz(parsedate_tz(ts.strip())))
	print dt
	ts = 'Fri Dec 07 16:12:48 +0000 2012'
	dt = int(mktime_tz(parsedate_tz(ts.strip())))
	print dt
	
if __name__ == '__main__':
	main()
		
	