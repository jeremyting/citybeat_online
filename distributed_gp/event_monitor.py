
#read tf-idf
# while 
#   search db
#   if e not classified
#       classify e. 
#       if e is event:
#           put it back to front-end db

from utility.event_interface import EventInterface
from utility.base_feature import BaseFeature
from utility.corpus import buildAllCorpus
from utility.region import Region
from utility.event import Event
import classifier
import time

class EventMonitor():
    def __init__(self, candidate_db, candidate_collection, classified_event_db, classified_event_collection, event_backup_db, event_backup_collection):
        self.candidate_db = candidate_db
        self.candidate_collection = candidate_collection
        self.classified_event_db = classified_event_db
        self.classified_event_collection = classified_event_collection
        self.event_backup_db = event_backup_db
        self.event_backup_collection = event_backup_collection 

        self.all_corpus = buildAllCorpus( time_interval_length = 2)
        self.clf = classifier.Classifier() 

    def goThroughCandidateDB(self):
        """Go through candidate event db and classify whatever is left"""
        ei = EventInterface(self.candidate_db, self.candidate_collection)
        ei_classified = EventInterface(self.classified_event_db, self.classified_event_collection)
        ei_backup = EventInterface(self.event_backup_db, self.event_backup_collection)
        cnt = 0
        
        for e in ei.getAllDocuments():
            e = Event(e)
            print 'working on ',cnt
            cnt+=1
            region = Region(e.getRegion())
            corpus = self.all_corpus[region.getKey()]
            ef = BaseFeature(e, corpus)     
            prob = self.clf.classify(ef.extractFeatures())
            
            ei_backup.addEvent(e)
            ei.deleteEventByID(str(e.getID()))
            if prob > 0.7:
                print 'ready to insert'
                e.setLabel( prob )
                ei_classified.addEvent(e)
            
    def monitor(self):
        em = EventMonitor('citybeat', 'candidate_event_15by15_merged',  'citybeat', 'instagram_front_end_events', 'citybeat', 'event_backup_instagram')
        while True:
            self.goThroughCandidateDB()
            time.sleep(60)

def test():
    em = EventMonitor('citybeat', 'candidate_event_15by15_merged',  'citybeat', 'instagram_front_end_events', 'citybeat', 'event_backup_instagram')
    em.goThroughCandidateDB()

if __name__=='__main__':
    test()
