import config
import types

from datetime import datetime
from mongodb_interface import MongoDBInterface
from config import InstagramConfig

class PredictionInterface(MongoDBInterface):
	
	def __init__(self, db=InstagramConfig.prediction_db,  
	             collection=InstagramConfig.prediction_collection):
		# initialize an interface for accessing photos from mongodb
		super(PredictionInterface, self).__init__()
		self.setDB(db)
		self.setCollection(collection)
		
	def getMostRecentPrediction(self, region):
		# THIS METHOD MUST BE UPDATED WHEN PUT INTO PRACTICE
		# TODO: within one hour
		# region should an instance of the class Region defined in region.py
		if not type(region) is types.DictType:
			region = region.toJSON()
		predictions = self.getAllDocuments({'region':region}).sort('time', -1)
		for prediction in predictions:
			return prediction
		raise Exception('no prediction is found')
		
	def getNearestPrediction(self, region, utc_time):
		# given t, find the most nearest prediction whose time is greater than or equal to t.
		# utc_time should a string (or unicode)
		if not type(region) is types.DictType:
			region = region.toJSON()
		utc_time = str(utc_time)
		condition = ({'region.min_lat':region['min_lat'],
			            'region.min_lng':region['min_lng'],
			            'region.max_lat':region['max_lat'],
			            'region.max_lng':region['max_lng']})
		condition['time'] = {'$gte':str(utc_time)}
		predictions = self.getAllDocuments(condition).sort('time', 1)
		for prediction in predictions:
			prediction_end_time = int(prediction['time'])
			prediction_begin_time = prediction_end_time - 3600
			cur_time = int(utc_time)
			if cur_time <=  prediction_end_time and prediction_begin_time <= cur_time:
				return prediction
#			return None
		return None

if __name__=="__main__":
	pi = PredictionInterface()
	pi.setDB('citybeat')
	pi.setCollection('online_prediction')
	
	region = {'min_lat': 40.775415479999999, 
		        'max_lng': -73.970081919999998, 
		        'min_lng': -73.978088200000002, 
		        'max_lat': 40.780720760000001}
	
	condition = ({'region.min_lat':region['min_lat'],
		          'region.min_lng':region['min_lng'],
		          'region.max_lat':region['max_lat'],
		          'region.max_lng':region['max_lng']})
	prediction = pi.getNearestPrediction(region, '1361768528') #1361772000
	print prediction
	
