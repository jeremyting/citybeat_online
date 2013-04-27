from event_interface import EventInterface
from event import Event
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from math import sqrt
from photo import Photo
from tweet import Tweet
from bson.objectid import ObjectId
from base_feature import BaseFeature

import numpy as np
from scipy.sparse import *
from sklearn.metrics.pairwise import linear_kernel

from corpus import Corpus
from corpus import buildAllCorpus
from region import Region

import copy
import tool

import re

class Representor():
    def __init__(self, element_type):
        """Given an event, return a list incices of the photos in 'photos' filed 
        which are representative to stands for this cluster
        
        Could overwrite TfidfVectorizer as a parameter so that you could customize
        your own tfidf parameters. 
        see http://scikit-learn.org/dev/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
        """
        
        assert element_type in ['tweets', 'photos']
        self._element_type = element_type
        
        paras = {}
        paras['max_df'] = 0.05
        paras['min_df'] = 1
        paras['strip_accents'] = 'ascii'
        paras['smooth_idf'] = True
        paras['preprocessor'] = self._preProcessor
        paras['sublinear_tf'] = True
        paras['norm'] = 'l2'
        paras['analyzer'] = 'char_wb'
        paras['ngram_range'] = (4,4)
        paras['stop_words'] = 'english'
        self._corpus_dicts_char = buildAllCorpus(debug=True, element_type=self._element_type, paras=paras)

        #paras['analyzer'] = 'word'
        #paras['ngram_range'] = (1,1)
        #paras['preprocessor'] = tool.textPreprocessor
        #self._corpus_dicts_word = buildAllCorpus(element_type=self._element_type, paras=paras)

    def _preProcessor(self, text):
        regex = re.compile(r"#\w+")
        match = regex.findall(text)
        if len(match)>=5:
            return ""
        else:
            return text

    def _getAllText(self):
        _text = []
        for event in self.events:
            _text += self._getEventText(event)
        return _text

    def _is_ascii(self, _str):
        return all(ord(c) < 128 for c in _str)

    def _getEventText(self, event):
        """For a given event, return the text as a list. Note for photo without text,
        use a None to hold the place"""
        
        assert self._element_type in Event(event).toDict().keys()
        
        event_text = []
        for element in event[self._element_type]:
            if self._element_type == 'photos':
                element = Photo(element)
            else:
                element = Tweet(element)
            try:
                if self._is_ascii(element.getText()):
                    event_text.append(element.getText().lower())
                else:
                    event_text.append("")
            except:
                event_text.append( "" )
        return event_text
        
    def _cosine_sim(self, a, b):
        return a*b.T
    
    def _getEventCharCorpus(self, event):
        region = Region(Event(event).toDict()['region'])
        return self._corpus_dicts_char[region.getKey()]
        
    def _getEventWordCorpus(self, event):
        region = Region(Event(event).toDict()['region'])
        return self._corpus_dicts_word[region.getKey()]  
    
    def getRepresentivePhotos(self, event):
       
        event_text = self._getEventText(event)
        corpus = self._getEventCharCorpus(event)
        event_tfidf = corpus.getVectorizer().transform(event_text)
        
        centroid = event_tfidf.mean(axis=0)
        #cosine_similarities = linear_kernel(centroid, event_tfidf).flatten()
        cosine_similarities = np.asarray(self._cosine_sim(centroid, event_tfidf)).flatten()

        most_related_pics = cosine_similarities.argsort()
        photos_to_return = []
        #print event['_id']
        for idx in most_related_pics:
#            print cosine_similarities[idx], event['photos'][idx]['link']
            photos_to_return.append( event['photos'][idx] )
        photos_to_return.reverse() 

        return photos_to_return 

    def getRepresentiveKeywords(self, event, k=5):
        # this method is invalid now
        event_text = self._getEventText(event)
        corpus = self._getEventWordCorpus(event)
        vectorizer = corpus.getVectorizer()
        voc = vectorizer.get_feature_names()
        tf_vec = vectorizer.transform(event_text).mean(axis=0)

        nonzeros = np.nonzero(tf_vec)[1]
        res_list = nonzeros.ravel().tolist()[0] 

        #values = []
        words = []
        k = min(k, len(res_list))
        for i in xrange(0, k):
            ind = res_list[i]
            words.append( voc[ind] )
            #values.append( tf_vec[0,n] )

        return words
    
    def getRepresentiveKeywords2(self, event, k=5):
        photos = self.getRepresentivePhotos(event)
        l = min(10, len(photos))
        photos = photos[0:l]
        new_event = copy.deepcopy(Event(event).toDict())
        new_event = Event(new_event)
        new_event.setElements(photos)
        topwords = BaseFeature(new_event)._getTopWords(k=k)
        return topwords

    def getTfidfVector(self, event):
        # this method is invalid now
        voc = self.vectorizer.get_feature_names()
        tf_vec = self.vectorizer.transform(self._getEventText(event)).mean(axis=0)

        nonzeros = np.nonzero(tf_vec)[1]
        res_list = nonzeros.ravel().tolist()[0] 

        values = []
        words = []
        for n in res_list:
            words.append( voc[n] )
            values.append( tf_vec[0,n] )

        return res_list, words, values

    def getCorpusWordsVector(self):
        # this method is invalid now
        return self.vectorizer.get_feature_names()

def test():
    rep = Representor('photos')
#    ei = EventInterface()
#    ei.setDB('citybeat')
#    ei.setCollection('candidate_event_25by25_merged')
#    cur = ei.getAllDocuments()
    events = getAllActualEvents()
    for event in events:
        print rep.getRepresentiveKeywords2(event)
        #print rep.getRepresentivePhotos(event)
        #
#        try:
#            print rep.getRepresentiveKeywords2(event)
#        except:
#            print rep._getEventText(event)
            
def getAllActualEvents():
    
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
            
    fid.close()
    return true_events
def main():
    #read labels and ids
    lines = open('label_data_csv2.txt').readlines()
    positive = []
    negative = []
    for line in lines:
        t = line.split()
        if t[1]=='1':
            positive.append(t[0])
        elif t[1]=='-1':
            negative.append(t[0])
    rep = Representor()
    #print rep.getCorpusWordsVector()


 
    
    for id in positive:
        for e in rep.events:
            if id == str(e['_id']):
                for p in rep.getRepresentivePhotos(e)[:10]:
                    pass
                    #print p['link']
                #print rep.getTfidfVector(e)
#                print '\n'

if __name__ == '__main__':
    test()
