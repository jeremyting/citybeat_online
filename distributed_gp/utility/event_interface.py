##########
# Author: Chaolun Xia, 2013-Jan-09#
#
# A high level interface to access the alarm data, for labeling the event
##########
#Edited by: (Please write your name here)#

from mongodb_interface import MongoDBInterface
from config import InstagramConfig
from datetime import datetime
from bson.objectid import ObjectId
from tweet_event import TweetEvent
from photo_event import PhotoEvent
import tool

import config
import time
import logging
import string
import types

class EventInterface(MongoDBInterface):
    
    def __init__(self, db=InstagramConfig.event_db,  
                 collection=InstagramConfig.event_collection):
      # initialize an interface for accessing event from mongodb
      super(EventInterface, self).__init__()
      self.setDB(db)
      self.setCollection(collection)
    
    def saveDocument(self, raw_event):
        #rewrite the method
        self.addEvent(raw_event)
        
    def getEventByID(self, ID):
        return self.getDocument({'_id':ObjectId(str(ID))})
    
    def deleteEventByID(self, ID):
        assert type(ID) is types.StringType
        self._deleteDocument({'_id':ObjectId(ID)})

    def addEventWithoutMerge(self, raw_event):
        super(EventInterface, self).saveDocument(raw_event)
    
    def addEvent(self, raw_event):
        # do not call the method saveDocument, instead, call this method
        # add an event to the db. raw_event can either be a json or an instance of Event 
        if not type(raw_event) is types.DictType:
            new_event = raw_event.toDict()
        else:
            new_event = raw_event

        event_type = tool.getEventType(new_event)

        if event_type == 'photos':
            new_event = PhotoEvent(new_event)
        else:
            new_event = TweetEvent(new_event)

        new_event.sortElements()
        new_event = new_event.toDict()
        # before adding, find if any event can be merged
        region = new_event['region']
        condition = ({'region.min_lat':region['min_lat'],
                        'region.min_lng':region['min_lng'],
                        'region.max_lat':region['max_lat'],
                        'region.max_lng':region['max_lng']})
#       condition = {'region.' + k:v for k,v in region.items()}
        old_events = self.getAllDocuments(condition).sort('created_time', -1)
        
        for old_event in old_events:
            end_time1 = int(new_event[event_type][0]['created_time'])
            begin_time1 = int(new_event[event_type][-1]['created_time'])
            end_time2 = int(old_event[event_type][0]['created_time'])
            begin_time2 = int(old_event[event_type][-1]['created_time'])
            time_interval = InstagramConfig.merge_time_interval
#           print 'new: ',end_time1,begin_time1
#           print 'old: ',end_time2,begin_time2
            if end_time1 + time_interval >= begin_time2 and end_time2 + time_interval >= begin_time1:
                # if can merge
                if event_type == 'photos':
                    merged_event = PhotoEvent(old_event)
                else:
                    merged_event = TweetEvent(old_event)
                merged = merged_event.mergeWith(new_event)        
                if merged >= 0:
                    print '%d out of %d %s are merged into an old event' % (merged, 
                                                                           len(new_event[event_type]),
                                                                           event_type)
#                   print old_event['_id'], new_event['_id']
                if merged > 0:
                    self.updateDocument(merged_event)
                return merged_event
        # cannot merge
        print 'create a new event'
        super(EventInterface, self).saveDocument(new_event)
        return new_event
      

def testDeleteEventByID():
    
    ei = EventInterface()
    ei.setDB('test')
    ei.setCollection('test_xia')
    ei.deleteEventByID('51147e8cc2a3754cfe668a86')
    cur = ei.getAllDocuments()
    print cur.count()
    for event in cur:
        print event['_id']
        
def TransferEvent():
    ei = EventInterface()
    ei.setDB('citybeat')
    ei.setCollection('candidate_event_25by25')
    
    ei2 = EventInterface()
    ei2.setDB('test')
    ei2.setCollection('test_useless')
    
    cur = ei.getAllDocuments()
    for event in cur:
        ei2.addEvent(event)

if __name__=='__main__':
    # TransferEvent()
    ei = EventInterface()
    ei.setDB('citybeat')
    ei.setCollection('candidate_event_25by25')
    for event in ei.getAllDocuments():
        e = PhotoEvent(event)
        print e.getGeoLocationCenter()
