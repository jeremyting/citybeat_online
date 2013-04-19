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


from utility.event_interface import EventInterface
from utility.event import Event


class Alarm():
    def __init__(self, region, start_time, end_of_time, prediction_collection, candidate_collection):
        self.cur_time = int(start_time)
        self.end_of_time = int(end_of_time)
        self.region = region
        self.prediction_collection = prediction_collection
        self.candidate_collection = candidate_collection

    def getNearestPrediction(self):
        pi = PredictionInterface()
        pi.setDB('citybeat_production')
        pi.setCollection('online_prediction')
        self.region.display()
        print str(self.cur_time)
        return pi.getNearestPrediction(self.region, str(self.cur_time))

    def _getFiftenMiniutesPhotos(self):
        pi = PhotoInterface( )
        _fifteen_minutes_ago = 15*60
        cursor  = pi.rangeQuery( self.region , (str( self.cur_time - _fifteen_minutes_ago), str(self.cur_time)) )
        _photos = []
        for p in cursor:
            _photos.append( p )
        print 'in fiften minutes there are ',len(_photos)
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
            #print 'None data for this region: details as follow'
            #self.region.display()
            #print 'time:' ,self.cur_time
            print 'No prediction'
            return 
        else:
            print 'Data!'
        mu = float(prediction['mu'])/4.0
        std = float(prediction['std'])/4.0
        time_stamp = prediction['time']

        zscore = (self.current_value - mu)*1.0/std

        print 'trying'
        if zscore > 0:   #comment this
            print 'in alarm!'
            e = Event()
            e.setPredictedValues(mu, std)
            e.setZscore(zscore)
            e.setRegion(self.region)
            e.setCreatedTime(self.cur_time)
            e.setActualValue(self.current_value)

            for p in self.photos:
                e.addPhoto(p)
            #print 'current value ',4.0*self.current_value, ' predict = ',mu*4.0,' std = ',std*4.0
        
            ei = EventInterface( )
            ei.setCollection(self.candidate_collection)
            print e.getEarliestPhotoTime(),e.getLatestPhotoTime()
            #print e.toDict()['region']
            #ei.addEvent(e)
            ei.addEventWithoutMerge(e)
            # modified by xia


def run(data_source):
    assert(sys.argv[1] in ['twitter', 'instagram'])
    coordinates = [InstagramConfig.photo_min_lat,
            InstagramConfig.photo_min_lng,
            InstagramConfig.photo_max_lat,
            InstagramConfig.photo_max_lng
                 ]
    
    alarm_region_size = 25
    nyc_region = Region(coordinates)
    regions = nyc_region.divideRegions(alarm_region_size,alarm_region_size)
    
    if data_source == 'twitter':
        regions = nyc_region.filterRegions( region_list = regions, test=True, n=alarm_region_size, m = alarm_region_size, document_type='tweet')
    elif data_source == 'instagram':
        regions = nyc_region.filterRegions( region_list = regions, test=True, n=alarm_region_size, m = alarm_region_size, document_type = 'photo')
        

    cur_utc_time = getCurrentStampUTC() 

    print 'all regions',len(regions)
    for region in regions:
        start_of_time =  cur_utc_time
        end_of_time = cur_utc_time
        if data_source == 'twitter':
            alarm = Alarm(region, start_of_time, end_of_time, TwitterConfig.prediction_collection, TwitterConfig.event_collection)
        elif data_source == 'instagram':
            alarm = Alarm(region, start_of_time, end_of_time, InstagramConfig.prediction_collection, InstagramConfig.event_collection)
        region.display()
        alarm.fireAlarm()

if __name__ == "__main__":
    assert( sys.argv[1] in ['twitter', 'instagram'])
    if sys.argv[1] == 'twitter':
        run(data_source = 'twitter')
    elif sys.argv[1] == 'instagram':
        run(data_source = 'instagram')

