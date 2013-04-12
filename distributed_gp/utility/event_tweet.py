from mongodb_interface import MongoDBInterface
from tweet import Tweet
from region import Region
from base_event import BaseEvent

import operator
import string
import types

class Event(BaseEvent):
	# Event is for Instagram
	
	def __init__(self, event=None):
		# the input argument event should be a dictionary or python object
		super(Event, self).__init__('tweets', event)

				
	def addTweet(self, tweet):
		# when use this method, please keep adding tweet in chronologically increasing order
		self.addElement(tweet)
		
	def getTweetNumber(self):
		return self.getElementNumber()
		
	def selectOneTweetForOneUser(self):
		self.leaveOneElementForOneUser()
	
	def removeDuplicateTweets(self):
		self.removeDuplicateElements()
		
	def containKeywords(self, words, freq=1):
		for word in words:
			res = self.getTweetsbyKeyword(word.lower())
			if len(res) >= freq:
				return True
		return False
	
	def getTweetsbyKeyword(self, word):
		pass

	def sortTweets(self):
		self.sortElements()
	
	def mergeWith(self, event):
		if type(event) is types.DictType:
			event = Event(event)
		event = event.toDict()
		
		tweet_list1 = self._event['tweets'] 
		tweet_list2 = event['tweets']
		
		new_tweet_list = []
		l1 = 0
		l2 = 0
		merged = 0
		while l1 < len(tweet_list1) and l2 < len(tweet_list2):
			p1 = Tweet(tweet_list1[l1])
			p2 = Tweet(tweet_list2[l2])
			compare = p1.compare(p2)
			if compare == 1:
				new_tweet_list.append(tweet_list1[l1])
				l1 += 1
				continue
			
			if compare == -1:
				new_tweet_list.append(tweet_list2[l2])
				l2 += 1
				merged += 1
				continue
			
			# compare == 0
			new_tweet_list.append(tweet_list1[l1])
			l1 += 1
			l2 += 1
		
		while l1 < len(tweet_list1):
			new_tweet_list.append(tweet_list1[l1])
			l1 += 1
		
		while l2 < len(tweet_list2):
			new_tweet_list.append(tweet_list2[l2])
			l2 += 1
			merged += 1
		
		self._event['tweets'] = new_tweet_list
		# update actual value
		self.setActualValue(self._getActualValueByCounting())
		
		# do not change the order of the following code
		actual_value_1 = self._event['actual_value']
		actual_value_2  = event['actual_value']
		zscore1 = float(self._event['zscore'])
		zscore2 = float(event['zscore'])
		std1 = float(self._event['predicted_std'])
		std2 = float(event['predicted_std'])
		new_std = (std1 * actual_value_1 + std2 * actual_value_2) / (actual_value_1 + actual_value_2)
		new_zscore = (zscore1 * actual_value_1 + zscore2 * actual_value_2) / (actual_value_1 + actual_value_2)
		self.setZscore(new_zscore)
		new_mu = actual_value_1 - new_zscore * new_std
		self.setPredictedValues(new_mu, new_std)
		
		return merged
				
	def setRegion(self, region):
		if not type(region) is types.DictType:
			region = region.toDict()
		self._event['region'] = region
	
	def setTweets(self, tweets):
		# a set of json objects
		self._event['tweets'] = tweets
		
	def setCreatedTime(self, utc_time):
		self._event['created_time'] = str(utc_time)
		
	def setPredictedValues(self, mu, std):
		self._event['predicted_mu'] = float(mu)
		self._event['predicted_std'] = float(std)
		
	def setZscore(self, zscore):
		self._event['zscore'] = float(zscore)
		
	def setActualValue(self, actual_value):
		self._event['actual_value'] = int(actual_value)
	
	def setLabel(self, label='unlabeled'):
		self._event['label'] = label
	
	def toDict(self):
		return self._event
		
	def _test_print(self):
		print self._event['created_time'], 'tweets:'
		for tweet in self._event['tweets']:
			print tweet['created_time']
			
	def getLatestTweetTime(self):
		return self.getLatestElementTime()
		
	   
	def getEarliestTweetTime(self):
		return self.getEarliestElementTime()
		
def main():
	pass