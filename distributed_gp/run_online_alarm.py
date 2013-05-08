import time
import math
import sys

from datetime import datetime
from datetime import timedelta
import calendar
from uuid import uuid4

from utility.instagram_time_series import InstagramTimeSeries
from utility.region import Region
from utility.config import InstagramConfig
from utility.config import TwitterConfig
from rq import Queue, Connection
from redis import Redis
from do_gp import Predict


from gp_job import GaussianProcessJob
from utility.prediction_interface import PredictionInterface
from utility.prediction import Prediction
from utility.tool import getCurrentStampUTC

from utility.tool import processAsPeopleCount

from utility.photo_interface import PhotoInterface
from utility.tweet_interface import TweetInterface


from utility.event_interface import EventInterface
from utility.tweet_event import TweetEvent
from utility.photo_event import PhotoEvent


class Alarm():
    def __init__(self, region, start_time, end_of_time, prediction_collection, candidate_collection, data_source):
        self.cur_time = int(start_time)
        self.end_of_time = int(end_of_time)
        self.region = region
        self.prediction_collection = prediction_collection
        self.candidate_collection = candidate_collection
        self.data_source = data_source

    def getNearestPrediction(self):
        pi = PredictionInterface()
        pi.setDB('citybeat_production')
        if self.data_source == 'instagram':
            pi.setCollection('online_prediction_instagram')
        else:
            pi.setCreatedTime('online_prediction_twitter')
        self.region.display()
        return pi.getNearestPrediction(self.region, str(self.cur_time))

    def _getFiftenMiniutesData(self):
        data_interface = None
        if self.data_source=='twitter':
            data_interface = TweetInterface('citybeat_production', 'tweets')
        elif self.data_source == 'instagram':
            data_interface = PhotoInterface('citybeat_production', 'photos')
        _fifteen_minutes_ago = 15*60
        cursor = data_interface.rangeQuery( self.region , (str( self.cur_time - _fifteen_minutes_ago), str(self.cur_time)) )
        _data = []
        for p in cursor:
            _data.append(p)
        _data = sorted( _data, key=lambda k:k['created_time'] )
        before = len(_data)
        _data = processAsPeopleCount(_data)
        after = len(_data)
        self.current_value = after
        self.data = _data


    def nextTimeStep(self, step_length ):
        _cur_time = self.cur_time + step_length
        if _cur_time > self.end_of_time:
            return False
        else:
            self.cur_time = _cur_time
            return True
    
    def fireAlarm(self):
        prediction = self.getNearestPrediction()
        
        self._getFiftenMiniutesData()
        if prediction is None:
            print 'No prediction'
            return 
        else:
            print 'Data!'
        mu = float(prediction['mu'])/4.0
        std = float(prediction['std'])/4.0
        time_stamp = prediction['time']
        zscore = (self.current_value - mu)*1.0/std
        print 'cur value = ' ,self.current_value, 'zscore = ', zscore
        if zscore > 3.0 and self.current_value>5:   #comment this
            print 'in alarm!, cur value = ',self.current_value
            if self.data_source == 'twitter':
                e = TweetEvent()
                for dt in self.data:
                    e.addTweet(dt)
            elif self.data_source == 'instagram':
                e = PhotoEvent()
                for dt in self.data:
                    e.addPhoto(dt)
            
            e.setPredictedValues(mu, std)
            e.setZscore(zscore)
            e.setRegion(self.region)
            e.setCreatedTime(self.cur_time)
            e.setActualValue(self.current_value)

            ei = EventInterface( )
            ei.setCollection(self.candidate_collection)
            print e.getEarliestPhotoTime(),e.getLatestPhotoTime()
            print ei.addEvent(e)


def run(data_source):
    coordinates = [InstagramConfig.photo_min_lat,
            InstagramConfig.photo_min_lng,
            InstagramConfig.photo_max_lat,
            InstagramConfig.photo_max_lng
                 ]
    
    alarm_region_size = 25
    nyc_region = Region(coordinates)
    regions = nyc_region.divideRegions(alarm_region_size,alarm_region_size)
    
    if data_source == 'twitter':
        regions = nyc_region.filterRegions( region_list = regions, test=True, n=alarm_region_size, m = alarm_region_size, element_type= 'tweets')
    elif data_source == 'instagram':
        regions = nyc_region.filterRegions( region_list = regions, test=True, n=alarm_region_size, m = alarm_region_size, element_type = 'photos')
        
    cur_utc_time = getCurrentStampUTC() 

    for region in regions:
        start_of_time =  cur_utc_time
        end_of_time = cur_utc_time
        if data_source == 'twitter':
            alarm = Alarm(region, start_of_time, end_of_time, TwitterConfig.prediction_collection, TwitterConfig.event_collection, data_source)
        elif data_source == 'instagram':
            alarm = Alarm(region, start_of_time, end_of_time, InstagramConfig.prediction_collection, InstagramConfig.event_collection, data_source)
            #for test only
            #alarm = Alarm(region, start_of_time, end_of_time, InstagramConfig.prediction_collection, "tmp_remove", data_source)
        region.display()
        alarm.fireAlarm()

if __name__ == "__main__":
    assert( sys.argv[1] in ['twitter', 'instagram'])
    if sys.argv[1] == 'twitter':
        run(data_source = 'twitter')
    elif sys.argv[1] == 'instagram':
        run(data_source = 'instagram')

