__author__ = 'lenovo'


import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.photo_interface import PhotoInterface
from utility.tweet_interface import TweetInterface
from utility.tool import getCurrentStampUTC
from utility.config import StatsConfig

import stats_config
from stats_interfaces import InstagramStatsInterface
from stats_interfaces import TwitterStatsInterface

class Status(object):

    def __init__(self):
        # emty dictionary
        self._tweet_interface = TweetInterface()
        self._photo_interface = PhotoInterface()

    def getCurrentCountStats(self, type):
        assert  type in ['photos', 'tweets']
        stats = {}
        stats['type'] = type
        if type == 'photos':
            stats['index'] = StatsConfig.photo_count_index
            res = self._extractPhotoCount()
        else:
            stats['index'] = StatsConfig.tweet_count_index
            res = self._extractTweetCount()
        stats['current_count'] = res[0]
        stats['delta'] = res[1]
        stats['created_time'] = str(getCurrentStampUTC())
        return stats

    def _extractTweetCount(self):
        now = int(getCurrentStampUTC())
        # 5 seconds as the latency
        current_count = self._tweet_interface.rangeQuery(period=[now - 65, now - 5]).count()
        baseline_count = self._tweet_interface.rangeQuery(period=[now - 65 - 600, now - 65]).count() / 10.0
        if baseline_count == 0.0:
            return [current_count, stats_config.NO_BASE_LINE]
        else:
            return [current_count, (current_count - baseline_count) / baseline_count]

    def _extractPhotoCount(self):
        now = int(getCurrentStampUTC())
        current_count = int(self._photo_interface.rangeQuery(period=[now - 600, now]).count() / 10.0 + 0.5)
        baseline_count = self._photo_interface.rangeQuery(period=[now - 60 * 21, now - 60]).count() / 20.0
        if baseline_count == 0.0:
            return [current_count, stats_config.NO_BASE_LINE]
        else:
            return [current_count, (current_count - baseline_count) / baseline_count]

def main():
    stats = Status()

    instagram_stats_interface = InstagramStatsInterface()
    instagram_stats = stats.getCurrentCountStats('photos')
    instagram_stats_interface.saveDocument(instagram_stats)

    twitter_stats_interface = TwitterStatsInterface()
    twitter_stats = stats.getCurrentCountStats('tweets')
    twitter_stats_interface.saveDocument(twitter_stats)

if __name__ == '__main__':
    main()