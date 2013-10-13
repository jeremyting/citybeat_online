__author__ = 'lenovo'


import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.photo_interface import PhotoInterface
from utility.tweet_interface import TweetInterface
from utility.tool import getCurrentStampUTC
from utility.tweet import Tweet

import stats_config
from stats_interfaces import InstagramStatsInterface
from stats_interfaces import TwitterStatsInterface

class Stats(object):

    def __init__(self):
        # emty dictionary
        self._tweet_interface = TweetInterface()
        self._photo_interface = PhotoInterface()

    def getCurrentCountStats(self, type):
        assert type in ['photos', 'tweets']
        stats = {}
        if type == 'photos':
            res = self._extractPhotoCount()
        else:
            res = self._extractTweetCount()
        stats['current_count_per_minute'] = res[0]
        stats['delta'] = res[1]
        stats['created_time'] = str(getCurrentStampUTC())
        return stats

    def get24HoursCountStats(self, type):
        assert type in ['photos', 'tweets']
        stats = {}
        stats['current_24_hours_counts'] = self._extract24HoursCountsStats(type=type)
        stats['past_week_24_hours_counts'] = self._extract24HoursCountsStats(past_week=True, type=type)
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

    def _extract24HoursCountsStats(self, past_week=False, type='tweets'):
        now = int(getCurrentStampUTC())
        offset = 0
        if past_week:
            offset = 7 * 24
        count_during_past_24_hours = []
        for hour in xrange(24):
            end_time = now - 3600 * hour - offset
            begin_time = end_time - 3600
            if type == 'tweets':
                count_during_past_24_hours.append(self._tweet_interface.rangeQuery(period=[begin_time, end_time]).count())
            else:
                count_during_past_24_hours.append(self._photo_interface.rangeQuery(period=[begin_time, end_time]).count())
        return count_during_past_24_hours

    def _extractTweetTopMentions(self, k=10):
        # 10 minutes
        now = int(getCurrentStampUTC())
        time_span = 10 * 60
        end_time = now
        begin_time = end_time - time_span
        cur = self._tweet_interface.rangeQuery(period=[begin_time, end_time], field='text')
        return cur

def main():
    stats = Stats()

    instagram_stats_interface = InstagramStatsInterface()
    instagram_stats = stats.getCurrentCountStats('photos')
    instagram_stats_interface.saveDocument(instagram_stats)

    twitter_stats_interface = TwitterStatsInterface()
    twitter_stats = stats.getCurrentCountStats('tweets')
    twitter_stats_interface.saveDocument(twitter_stats)

if __name__ == '__main__':
    main()
