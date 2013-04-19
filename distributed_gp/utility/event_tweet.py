from mongodb_interface import MongoDBInterface
from tweet import Tweet
from region import Region
from base_event import BaseEvent

import operator
import string
import types

class TweetEvent(BaseEvent):
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
    
    def getTweetsByKeyword(self, word):
        return self.getElementsByKeyword(word)

    def sortTweets(self):
        self.sortElements()
    
    def setTweets(self, tweets):
        self.setElements(tweets)
            
    def getLatestTweetTime(self):
        return self.getLatestElementTime()
        
    def getEarliestTweetTime(self):
        return self.getEarliestElementTime()
    
    # will not be used for feature extraction
    def mergeWith(self, event):
        self._mergeWith(TweetEvent(event))
        
def main():
    pass