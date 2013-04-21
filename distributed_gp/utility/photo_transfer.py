from event_interface import EventInterface
from base_feature import BaseFeature
from base_feature_sparse import BaseFeatureSparse
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from text_parser import TextParser
from stopwords import Stopwords
from corpus import Corpus
from representor import Representor

import operator
import string
import types
import random
import math

import sys

def transferPhoto():
    # remove duplicate
    pi = PhotoInterface()
    pi.setDB('tmp_citybeat')
    pi.setCollection('photos')
    
    pi2 = PhotoInterface()
    pi2.setDB('citybeat_production')
    pi2.setCollection('photos')
    
    photo_cur = pi.getAllDocuments()
    id_set = set()
    for photo in photo_cur:
        if photo['id'] not in id_set:
            id_set.add(photo['id'])
            photo['_id'] = photo['id']
            pi2.saveDocument(photo)
    
    print len(id_set)

if __name__=='__main__':
    transferPhoto()
    
    
    
    
    
    
    
    