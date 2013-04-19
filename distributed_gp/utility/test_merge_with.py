from event_interface import EventInterface
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from caption_parser import CaptionParser
from stopwords import Stopwords
from corpus import Corpus
from _kl_divergence import kldiv
from _kl_divergence import tokenize

import kl_divergence as KLDivergence

import operator
import string
import types
import random
import math
import numpy

def testWithMerge():
    ei = EventInterface()
    ei.setDB('citybeat')
    ei.setCollection('candidate_event_25by25')
    
    ei2 = EventInterface()
    ei2.setDB('test')
    ei2.setCollection('candidate_event')
    
    cur = ei.getAllDocuments()
    for event in cur:
       ei2.addEvent(event)
       

testWithMerge() 