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
#from utility.event import Event
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
        pi.setDB('citybeat_experiment')
        if self.data_source == 'twitter':
            pi.setCollection('twitter_prediction')
        elif self.data_source == 'instagram':
            pi.setCollection('instagram_prediction')
        return pi.getNearestPrediction(self.region, str(self.cur_time))

    def _getFiftenMiniutesPhotos(self):
        #pi = PhotoInterface('citybeat_experiment', 'tweets')
        data_interface = None
        if self.data_source=='twitter':
            data_interface = TweetInterface('citybeat_production', 'tweets')
        elif self.data_source == 'instagram':
            data_interface = TweetInterface('citybeat_production', 'photos')
        _fifteen_minutes_ago = 15*60
        #cursor  = pi.rangeQuery( self.region , (str( self.cur_time - _fifteen_minutes_ago), str(self.cur_time)) )
        cursor = data_interface.rangeQuery( self.region , (str( self.cur_time - _fifteen_minutes_ago), str(self.cur_time)) )
        _photos = []
        for p in cursor:
            _photos.append(p)
        _photos = sorted( _photos, key=lambda k:k['created_time'] )
        before = len(_photos)
        _photos = processAsPeopleCount(_photos)
        after = len(_photos)
        self.current_value = after
        self.photos = _photos

    def nextTimeStep(self, step_length ):
        _cur_time = self.cur_time + step_length
        if _cur_time > self.end_of_time:
            return False
        else:
            self.cur_time = _cur_time
            return True
    
    def fireAlarm(self):
        prediction = self.getNearestPrediction()
        
        self._getFiftenMiniutesPhotos()
        if prediction is None:
            print 'None data for this region: details as follow'
            self.region.display()
            print 'time:' ,self.cur_time
            return 
        mu = float(prediction['mu'])/4.0
        std = float(prediction['std'])/4.0
        time_stamp = prediction['time']

        zscore = (self.current_value - mu)*1.0/std

        print 'zscore = ',zscore, 'pred_mu = ',mu, 'actual = ',self.current_value
        if zscore > 3 and self.current_value>=8:
            if self.data_source=='twitter':
                e = TweetEvent()
            elif self.data_source == 'instagram':
                e = PhotoEvent()     #this is default instagram event
            e.setPredictedValues(mu, std)
            e.setZscore(zscore)
            e.setRegion(self.region)
            e.setCreatedTime(self.cur_time)
            e.setActualValue(self.current_value)

            for p in self.photos:
                e.addTweet(p)
            #print 'current value ',4.0*self.current_value, ' predict = ',mu*4.0,' std = ',std*4.0
        
            ei = EventInterface( )
            ei.setDB('citybeat_experiment')
            ei.setCollection(self.candidate_collection)
            #print e.getEarliestPhotoTime(),e.getLatestPhotoTime()
            #print e.toDict()['region']
            ei.addEvent(e)
            #ei.addEventWithoutMerge(e)
            # modified by xia


def run( data_source):
    coordinates = [InstagramConfig.photo_min_lat,
            InstagramConfig.photo_min_lng,
            InstagramConfig.photo_max_lat,
            InstagramConfig.photo_max_lng
                 ]
    huge_region = Region(coordinates)
    
    alarm_region_size = 25

    regions = huge_region.divideRegions(alarm_region_size,alarm_region_size)
    prediction_collection = None
    candidate_collection = None
    if data_source == 'twitter':
        element_type = 'tweets'
        prediction_collection = "twitter_prediction"
        candidate_collection = "twitter_candidate_events"
    elif data_source == 'instagram':
        element_type = 'photos'
        prediction_collection = "instagram_prediction"
        candidate_collection = "instagram_candidate_events"

    filtered_regions = huge_region.filterRegions( regions, test=True, n=25, m=25, element_type=element_type)
    # get the same regions as in db. Here it's 10 by 10

    regions = filtered_regions
    test_cnt = 0
    print 'all regions',len(regions)
    for region in regions:
        #delete the last 7*24*3600 to set it back to Dec 1st
        start_of_time =  1367107200
        end_of_time = 1367107200 + 7*24*3600 
        alarm = Alarm(region, start_of_time, end_of_time, prediction_interface, candidate_collection, data_source)
        cnt = 0
        region.display()
        xia_cnt = 0
        while alarm.nextTimeStep(300):
            cnt += 1
            alarm.fireAlarm()
            if cnt%100==0:
                print 'cur = ', time.gmtime(float(alarm.cur_time) )
                print 'alarm = ',cnt
        print '\n\n' 
if __name__ == "__main__":
    assert(sys.argv[1] in ['twitter', 'instagram'])
    data_source = sys.argv[1]
    
    run( data_source)                            
