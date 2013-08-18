from utility.base_event import BaseEvent


class TweetEvent(BaseEvent):
    # Event is for Instagram

    def __init__(self, event=None):
        # the input argument event should be a dictionary or python object
        super(TweetEvent, self).__init__('tweets', event)


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
        return self._mergeWith(TweetEvent(event))


def main():
    TweetEvent()