from event_interface import EventInterface
from base_feature import BaseFeature
from base_feature_production import BaseFeatureProduction
from region import Region
from event import Event
from text_parser import TextParser
from stopwords import Stopwords
from bson.objectid import ObjectId
from corpus import Corpus
from corpus import buildAllCorpus
from representor import Representor

import operator
import string
import types
import random
import math

import sys

def loadUnbalancedData():
    # load modified 
    
    ei = EventInterface()
    ei.setDB('citybeat')
    ei.setCollection('candidate_event_25by25_merged')
    
    true_events = []
    false_events = []
    fid2 = open('labeled_data_cf/181_positive.txt', 'r')
        
    modified_events = {}
    
    for line in fid2:
        t = line.split(',')
        modified_events[str(t[0])] = int(t[1])
    fid2.close()
        
    # put the data into a text file first
    fid = open('labeled_data_cf/data2.txt','r')
    for line in fid:
        if len(line.strip()) == 0:
            continue
        t = line.strip().split()
        if not len(t) == 3:
            continue
        label = t[0].lower()
        confidence = float(t[1])
        event_id = str(t[2].split('/')[-1])
        if label == 'not_sure':
            continue
        if label == 'yes':
            label = 1
        else:
            label = -1
        event = ei.getDocument({'_id':ObjectId(event_id)})
        event['label'] = label
        if modified_events.has_key(event_id):
            event['label'] = modified_events[event_id]
        
        e = Event(event)
        if e.getActualValue() < 8 or event['label'] == 0:
#           print 'bad event ' + id
            continue
        if event['label'] == 1:
            true_events.append(event)
        else:
            if event['label'] == -1 and confidence == 1:
                false_events.append(event)
            
    fid.close()
    return true_events, false_events

def generateData2():
#   if sparse:
    #rep = Representor()

    all_corpus = buildAllCorpus(time_interval_length=14, debug=True)
    true_event_list, false_event_list = loadUnbalancedData()
    BaseFeatureProduction.GenerateArffFileHeader()
        
    for event in true_event_list + false_event_list:
        r = Region(event['region'])
        corpus = all_corpus[r.getKey()]
        BaseFeatureProduction(event, corpus, None).printFeatures()

def main():
	generateData2()

if __name__=='__main__':
	main()
    
    
    
    
    
    
    
    
    
    
    
    
    
#def loadRawLabeledData():
#   
#   ei = EventInterface()
#   ei.setDB('citybeat')
#   ei.setCollection('candidate_event_25by25_merged')
#   
#   true_events = []
#   false_events = []
#   
#   # put the data into a text file first
#   fid = open('labeled_data_cf/data2.txt','r')
#   np = 0
#   nn = 0
#   for line in fid:
#       if len(line.strip()) == 0:
#           continue
#       t = line.split()
#       if not len(t) == 3:
#           continue
#       label = t[0].lower()
#       confidence = float(t[1])
#       event_id = t[2].split('/')[-1]
#       if label == 'yes':
#           event = ei.getDocument({'_id':ObjectId(event_id)})
#           event['label'] = 1
#           true_events.append(event)
#       if label == 'no':
#           if confidence < 1:
#               continue
#           event = ei.getDocument({'_id':ObjectId(event_id)})
#           event['label'] = -1
#           if event['actual_value'] < 8:
#               continue
#           false_events.append(event)
#   fid.close()
#   return true_events, false_events
