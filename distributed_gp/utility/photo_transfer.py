from event_interface import EventInterface
from event_feature import EventFeature
from event_feature_sparse import EventFeatureSparse
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from caption_parser import CaptionParser
from stopwords import Stopwords
from bson.objectid import ObjectId
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
	
	
	
	
	
	
	
	