#!/usr/bin/python
# -*- coding: utf8 -*-

# the name of this file is mis-leading, it actually provides the stats data

import json
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.event_interface import EventInterface
from utility.event import Event
from utility.config import InstagramConfig
from utility.tool import getCurrentStampUTC
from stats.stats_interface import StatsInterface

#from utility.representor import Representor

import random

class Root:
    def __init__(self):
        self.ei = EventInterface()
        self.ei.setDB(InstagramConfig.event_db)
        #self.representor = Representor(db='citybeat_production', collection='instagram_front_end_events')
        
        self.ei.setCollection(InstagramConfig.front_end_events)
        self.stats_interface = StatsInterface()

    def getAllEvents(self):
        now = int(getCurrentStampUTC())
        two_days_before = now - 3 * 24 * 3600
        event_cursor = self.ei.getAllDocuments({'created_time':{'$gte':str(two_days_before)}})
        events = []
        for e in event_cursor:
            #representor
            #rep_photos = self.representor.getRepresentivePhotos(e)
            #e['photos'] = rep_photos[:min(5,len(rep_photos))]
            e['_id'] = str(e['_id'])
            e['urgency'] = 58
            e['volume'] = 99
            e['stats'] = {'photos':50, 'tweets':0, 'checkins':0}
            #print e['photos']
            if e['actual_value']>=6 and e['zscore']>3.0:
                events.append(e)
        events = sorted(events, key = lambda x:x['created_time'], reverse=True)
        for w in events:
            print w['created_time']
        events = events[:5]
        return json.dumps(events)
    getAllEvents.exposed = True 
    
    def getAllEventsIDs(self):
        object_ids = self.ei.getAllDocumentIDs()
        return_value = []
        for _id in object_ids:
            return_value.append( str(_id) )
        return json.dumps( return_value )
    #getAllEventsIDs.exposed = True
    
    def getPhotosByID(self, event_id):
        event = json.loads(self.getEventByID(event_id))
        res = []
        all_photos = []
        top10_photos = []
        all_photos.append('all_photos')
        all_photos.append(len(event['photos']))
        all_photos.append( event['photos'])
        rep_photos = event['photos']
        top10_photos.append('top_10_representative')
        top10_photos.append(min(10, len(rep_photos)))
        top10_photos.append(rep_photos)
   
        res.append(all_photos)
        res.append(top10_photos)
        r = json.dumps(res) 
        return r
    getPhotosByID.exposed = True
   
    def getEventByID(self, event_id):
        event = self.ei.getEventByID(event_id)
        event = Event(event)
        event.selectOnePhotoForOneUser()
        event_dic = event.toDict()
        event_dic['_id'] = str(event_dic['_id'])
        return json.dumps(event_dic)
    getEventByID.exposed = True
    
    def setLabel(self, event_id, label):
        event = self.ei.getEventByID(str(event_id))
        event['label'] = int(label)
        self.ei.updateDocument( event )
    #setLabel.exposed = True

    def getLatestStats(self):
        now = int(getCurrentStampUTC()) - 5 * 60
        condition = {'created_time': {"$gte": str(now)}}
        most_recent_stats = self.stats_interface.getAllDocuments(condition=condition).sort('created_time', -1)[0]
        most_recent_stats['_id'] = str(most_recent_stats['_id'])
        return json.dumps(most_recent_stats)
    getLatestStats.exposed = True

e = Root()
print e.getLatestStats()

