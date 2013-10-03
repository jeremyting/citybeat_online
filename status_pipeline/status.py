__author__ = 'lenovo'


import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.photo_interface import PhotoInterface
from utility.tweet_interface import TweetInterface
from  utility.tool import getCurrentStampUTC

import status_config

class Status(object):

    def __init__(self):
        # emty dictionary
        self._status = {}
        self._tweet_interface = TweetInterface()
        self._photo_interface = PhotoInterface()

    def extractInstagramStatus(self):
        pass

    def extractTweetStatus(self):
        pass

    def _extractTweetCount(self):
        now = int(getCurrentStampUTC())
        current_count = self._tweet_interface.rangeQuery(period=[now - status_config.current_period, now]).count()
        baseline_count = self._tweet_interface.rangeQuery(period=[now - status_config.base_period - status_config.current_period, now - status_config.current_period]).count()
        return [current_count, (current_count * (status_config.base_period * 1.0 / status_config.current_period) - baseline_count) / baseline_count]

    def _extractPhotoCount(self):
        now = int(getCurrentStampUTC())
        current_count = self._photo_interface.rangeQuery(period=[now - status_config.current_period, now]).count()
        baseline_count = self._photo_interface.rangeQuery(period=[now - status_config.base_period - status_config.current_period, now - status_config.current_period]).count()
        return [current_count, (current_count * (status_config.base_period * 1.0 / status_config.current_period) - baseline_count) / baseline_count]

def main():
    s = Status()
    print s._extractTweetCount()
    print s._extractPhotoCount()

main()