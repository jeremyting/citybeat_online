from email.utils import parsedate_tz, mktime_tz
from base_element import BaseElement

import operator
import string
import types
import time


class Tweet(BaseElement):
	
	def __init__(self, tweet):
		super(Tweet, self).__init__(tweet)
	
	def getCreatedUTCTimestamp(self):
		ts = self._element['created_at']
		dt = int(mktime_tz(parsedate_tz(ts.strip())))
		return str(dt)
		
	def getRawText(self):
		# need to consider if use lower()
		if 'text' not in self._element.keys():
			return ''
		return self._element['text'].strip()
		
	def getText(sefl):
		# # new interface
		return self.getRawText()
	
	def findKeywords(self, keywords):
		text = self.getRawText()
		occur = 0
		for word in keywords:
			if word in text:
				occur += 1
		return occur
	
	def getRetweetFreq(self):
		return int(self._element['retweet_count'])
		
def main():
	ts = 'Fri Dec 07 16:12:48 +0100 2012'
	dt = int(mktime_tz(parsedate_tz(ts.strip())))
	print dt
	ts = 'Fri Dec 07 16:12:48 +0000 2012'
	dt = int(mktime_tz(parsedate_tz(ts.strip())))
	print dt
	
if __name__ == '__main__':
	main()
		
	