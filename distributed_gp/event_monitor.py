
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

class EventMonitor():
    def __init__(self, db, collection):
        self.db = db
        self.collection = collection
        all_corpus = buildAllCorpus()

    def goThroughCandidateDB(self):
        """Go through candidate event db and classify whatever is left"""
        ei = EventInterface(self.db, self.collection)
        
        for e in ei.getAllDocuments():
            region = e['region']
            corpus = all_corpus[region.getKey()]
            ef = EventFeatureInstagram(e, corpus)
            print ef.extractFeatures()



em = EventMonitor('citybeat', 'candidate_event_25by25_merged')
em.goThroughCandidateDB()

