import os

instagram_client_id = '4d9231b411eb4ef69435b40eb83999d6'
instagram_client_secret = '204c565fa1244437b9034921e034bdd6'
instagram_API_pause = 0.1
mongodb_address = 'ec2-23-22-67-45.compute-1.amazonaws.com'
mongodb_port = 27017
production_back_end_db = 'citybeat_production'

mongodb_user = 'admin'
mongodb_password = 'mediumdatarules'

class BaseConfig(object):
    min_lat = 40.690531
    max_lat = 40.823163
    min_lng = -74.058151
    max_lng = -73.857994
    region_percentage = 0.3
    min_elements = 8

    # grand : res ; joust : grad
    @staticmethod
    def getRegionListPath():
        cp = os.getcwd()
        #relative path here
        path = os.path.join(os.path.dirname(__file__), 'region_cache/')
        return path


class InstagramConfig(BaseConfig):
    photo_db = production_back_end_db
    event_db = production_back_end_db
    prediction_db = production_back_end_db
    #online setting
    photo_collection = 'photos'
    event_collection = 'online_candidate_instagram'
    prediction_collection = 'online_prediction_instagram'
    front_end_events = 'instagram_front_end_events'
    # in seconds
    merge_time_interval = 1
    zscore = 3
    min_phots = 8
    # bottom left: 40.690531,-74.058151
    # bottom right: 40.823163,-73.857994
    photo_min_lat = 40.690531
    photo_max_lat = 40.823163
    photo_min_lng = -74.058151
    photo_max_lng = -73.857994
    # cut the region into region_N * region_M subregions
    # try 10*10, 15*15, 20*20, 25*25
    #region_N = 25
    #region_M = 25
    redis_server = 'tall3'


class TwitterConfig(BaseConfig):
    # we have not yet moved tweets from citybeat to production
    tweet_db = production_back_end_db
    event_db = production_back_end_db
    prediction_db = production_back_end_db
    tweet_collection = 'tweets'
    prediction_collection = 'online_prediction_twitter'
    event_collection = 'online_candidate_twitter'
    # store tweets contains NY, NYC, NEW YORK, NEW YORK CITY
    extended_tweet_collection = 'extended_tweets'
    # grand : res ; joust : grad

class StatsConfig(object):
    instagram_collection = 'instagram_stats'
    twitter_collection = 'twitter_stats'

if __name__ == '__main__':
    print BaseConfig.getRegionListPath()
