##########
# Author: Chaolun Xia, 2013-Jan-09#
#
# A high level interface to access the alarm data, for labeling the event
##########
#Edited by: (Please write your name here)#

from mongodb_interface import MongoDBInterface
from tweet import Tweet
from config import TwitterConfig
from datetime import datetime
from bson.objectid import ObjectId

import config
import time
import logging
import string
import types
import json
import numpy


class ElementInterface(MongoDBInterface):
    # inner class only provide unified rangeQuery


    def __init__(self, db, collection, element_type):
      # initialize an interface for accessing event from mongodb
      super(ElementInterface, self).__init__()
      self.setDB(db)
      self.setCollection(collection)
      self._element_type = element_type

      
    
    def rangeQuery(self, region=None, period=None):
        #period should be specified as: [begin_time end_time]
        #specify begin_time and end_time as the utctimestamp, string!!
        
        if period is not None:
            assert period[0] <= period[1]
        
        region_conditions = {}
        period_conditions = {}
        if not region is None:
        #region should be specified as the class defined in region.py
            if not type(region) is types.DictType:
                region = region.toDict() 
            region_conditions = {'location.latitude':{'$gte':region['min_lat'], '$lte':region['max_lat']},
                                   'location.longitude':{'$gte':region['min_lng'], '$lte':region['max_lng']}
                                    }
                                    
        if not period is None:
            period_conditions = {'created_time':{'$gte':str(period[0]), '$lte':str(period[1])}}

        conditions = dict(region_conditions, **period_conditions)
        
        #returns a cursor
        #sort the tweet in chronologically decreasing order
        return self.getAllDocuments(conditions).sort('created_time', -1)
