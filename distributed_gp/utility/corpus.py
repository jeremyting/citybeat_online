from event_interface import EventInterface
from caption_parser import CaptionParser
from photo import Photo
from stopwords import Stopwords

from photo_interface import PhotoInterface
from tweet_interface import TweetInterface
from photo import Photo
from tweet import Tweet
from region import Region
from config import InstagramConfig
from config import TwitterConfig
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import tool

import random
import time
from datetime import datetime


import time
import math
import operator

class Corpus(object):

    def buildCorpus(self, region, time_interval, document_type='photo'):
        # time_interval should be [start, end]
        if document_type == 'photo':
            di = PhotoInterface()
        else:
            di = TweetInterface()
        cur = di.rangeQuery(region, time_interval)
        text = []
        for document in cur:
            if document_type == 'photo':
                doc = Photo(document)
            else:
                doc = Tweet(document)
            t = doc.getText()
            #at least 5 length
            if len(t) > 4:
                text.append(t)
        # it is not proper here to set up stopwords
        self._vectorizer = TfidfVectorizer(max_df=0.20, min_df=0, strip_accents='ascii',
                                           preprocessor=tool.textPreprocessor,
                                                 smooth_idf=True, sublinear_tf=True, norm='l2', 
                                                                       analyzer='word', ngram_range=(1,1), stop_words = 'english')
        self._vectorizer.fit_transform(text)
            
    def chooseTopWordWithHighestTDIDF(self, text, k=10):
        voc = self._vectorizer.get_feature_names()
        tf_vec = self._vectorizer.transform([text]).mean(axis=0)
        nonzeros = np.nonzero(tf_vec)[1]
        res_list = nonzeros.ravel().tolist()[0] 
        values = []
        words = []
        for n in res_list:
            words.append( voc[n] )
            values.append( tf_vec[0,n] )
        while len(values) < k:
            values.append(0)
        #return res_list, words, values
        return values


def buildAllCorpus(element_type='photos', time_interval_length=14):
    # return a dict = {region : its local corpus}
    assert element_type in ['photos', 'tweets']
    
    all_corpus = {}
    if element_type == 'photos':
        coordinates = [InstagramConfig.photo_min_lat, InstagramConfig.photo_min_lng,
                       InstagramConfig.photo_max_lat, InstagramConfig.photo_max_lng]
    else:
        coordinates = [TwitterConfig.min_lat, TwitterConfig.min_lng,
                       TwitterConfig.max_lat, TwitterConfig.max_lng]
                                     
    nyc = Region(coordinates)
    region_list = nyc.divideRegions(25, 25)
    region_list = nyc.filterRegions(region_list, test=True, n=25, m=25, document_type=document_type)
    
    # 14 days ago
    now = int(tool.getCurrentStampUTC()) - 40 *3600 *24
    
    num = 0
    for region in region_list:
        cor = Corpus()
        cor.buildCorpus(region, [now - time_interval_length *3600 *24, now], document_type)
        all_corpus[region.getKey()] = cor
        num += 1
        print 'build corpus %d' % (num)  
    return all_corpus

if __name__ == '__main__':
    buildAllCorpus()