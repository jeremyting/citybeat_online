
#read tf-idf
# while 
#   search db
#   if e not classified
#       classify e. 
#       if e is event:
#           put it back to front-end db

from utility.event_interface import EventInterface
from utility.event_feature_instagram import EventFeatureInstagram
from utility.corpus import buildAllCorpus
from utility.region import Region
import classifier

class EventMonitor():
    def __init__(self, candidate_db, candidate_collection):
        self.candidate_db = candidate_db
        self.candidate_collection = candidate_collection
        self.all_corpus = buildAllCorpus( time_interval_length = 14)
        self.clf = classifier.Classifier() 

    def goThroughCandidateDB(self):
        """Go through candidate event db and classify whatever is left"""
        ei = EventInterface(self.candidate_db, self.candidate_collection) 
        cnt = 0
        for e in ei.getAllDocuments():
            print 'working on ',cnt
            cnt+=1
            region = Region(e['region'])
            corpus = self.all_corpus[region.getKey()]
            # note that ef[-1] is the id of that event
            ef = EventFeatureInstagram(e, corpus)
            
            self.clf.classify(ef.extractFeatures())
            is_event = 1.0
            if is_event :
                #store event into db
                pass
            

em = EventMonitor('citybeat', 'next_week_candidate_event_25by25_merged')
em.goThroughCandidateDB()

