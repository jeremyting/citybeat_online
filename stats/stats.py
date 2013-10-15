__author__ = 'lenovo'


import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.photo_interface import PhotoInterface
from utility.tweet_interface import TweetInterface
from utility.tool import getCurrentStampUTC
from utility.tweet import Tweet
from utility.config import TwitterConfig

import stats_config
from stats_interface import StatsInterface

import re
import operator

class Stats(object):

    def __init__(self):
        # emty dictionary
        self._tweet_interface = TweetInterface()
        self._photo_interface = PhotoInterface()

    def getTweetAndPhotoStats(self):
        stats = {}
        tweet_basic_count = {}
        photo_basic_count = {}

        photo_basic_count['last_minute'] = self._getCurrentCountStats('photos')
        photo_basic_count['last_24_hour'] = self._get24HoursCountStats('photos')

        tweet_basic_count['last_minute'] = self._getCurrentCountStats('tweets')
        tweet_basic_count['last_24_hour'] = self._get24HoursCountStats('tweets')

        res = self._extractMostPopularTweet()
        stats['photo_basic_count'] = photo_basic_count
        stats['tweet_basic_count'] = tweet_basic_count
        stats['created_time'] = str(getCurrentStampUTC())
        stats['tweet_top_mentions'] = self._extractTweetTopMentions()
        stats['most_popular_tweet'] = res[0]
        stats['tweet_vs_retweet'] = res[1]
        return stats

    def _getCurrentCountStats(self, type):
        assert type in ['photos', 'tweets']
        stats = {}
        if type == 'photos':
            res = self._extractPhotoCount()
        else:
            res = self._extractTweetCount()
        stats['count'] = res[0]
        stats['delta'] = res[1]
        return stats

    def _get24HoursCountStats(self, type):
        assert type in ['photos', 'tweets']
        stats = {}
        stats['current_count'] = self._extract24HoursCountsStats(type=type)
        stats['last_week_count'] = self._extract24HoursCountsStats(past_week=True, type=type)
        return stats

    def _extractTweetCount(self):
        now = int(getCurrentStampUTC())
        # 5 seconds as the latency
        current_count = self._tweet_interface.rangeQuery(period=[now - 65, now - 5]).count()
        baseline_count = self._tweet_interface.rangeQuery(period=[now - 65 - 60 * 20, now - 65]).count() / 20.0
        if baseline_count == 0.0:
            return [current_count, stats_config.NO_BASE_LINE]
        else:
            return [current_count, (current_count - baseline_count) / baseline_count]

    def _extractPhotoCount(self):
        now = int(getCurrentStampUTC())
        offset = 4 * 60
        current_count = self._photo_interface.rangeQuery(period=[now - offset - 60, now - offset]).count()
        baseline_count = self._photo_interface.rangeQuery(period=[now - 60 * 21 - offset, now - offset - 60]).count() / 20.0
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
            end_time = now - 3600 * (hour + offset)
            begin_time = end_time - 3600
            if type == 'tweets':
                count_during_past_24_hours.append(self._tweet_interface.rangeQuery(period=[begin_time, end_time]).count())
            else:
                count_during_past_24_hours.append(self._photo_interface.rangeQuery(period=[begin_time, end_time]).count())
        return count_during_past_24_hours

    def _extractTweetTopMentions(self, k=10):
        # 60 minutes
        now = int(getCurrentStampUTC())
        time_span = 60 * 60
        end_time = now
        begin_time = end_time - time_span
        cur = self._tweet_interface.rangeQuery(period=[begin_time, end_time], fields=['text'])

        users = {}
        twitter_username_re = re.compile(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9_-]+)')
        for tweet in cur:
            text = tweet['text']
            mentions = twitter_username_re.findall(text)
            for mention in mentions:
                count = users.get(mention, 0) + 1
                users[mention] = count

        users = sorted(users.iteritems(), key=operator.itemgetter(1), reverse=True)
        res = []
        for key, value in users:
            res_pair = {}
            res_pair['user_name'] = key
            res_pair['count'] = value
            res.append(res_pair)
            if len(res) >= 10:
                break
        return res

    def _extractMostPopularTweet(self):
        ti = TweetInterface(collection=TwitterConfig.extended_tweet_collection)
        tweets = {}
        most_popular_tweet_text = ''
        max_retweet_count = -1
        user_name = ''

        # 60 minutes
        now = int(getCurrentStampUTC())
        time_span = 60 * 60
        end_time = now
        begin_time = end_time - time_span

        for tweet in ti.rangeQuery(period=[begin_time, end_time], fields=['text', 'user.screen_name']):
            text = tweet['text']
            count = tweets.get(text, 0) + 1
            tweets[text] = count
            if count > max_retweet_count:
                max_retweet_count = count
                most_popular_tweet_text = text
                user_name = tweet['user']['screen_name']

        single_tweet_count = 0
        retweet_count = 0
        for key, value in tweets.items():
            if value == 1:
                single_tweet_count += 1
            else:
                retweet_count += value

        most_popular_tweet = {}
        most_popular_tweet['user_name'] = user_name
        most_popular_tweet['text'] = most_popular_tweet_text
        most_popular_tweet['count'] = max_retweet_count

        tweets_count = {}
        tweets_count['tweet_percentage'] = 1.0 * single_tweet_count / (single_tweet_count + retweet_count)
        tweets_count['retweet_percentage'] = 1.0 * retweet_count / (single_tweet_count + retweet_count)

        return [most_popular_tweet, tweets_count]

def main():
    stats = Stats()
    si = StatsInterface()
    si.saveDocument(stats.getTweetAndPhotoStats())

if __name__ == '__main__':
    main()
