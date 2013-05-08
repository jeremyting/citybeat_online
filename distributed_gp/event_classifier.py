
#read tf-idf
# while 
#   search db
#   if e not classified
#       classify e. 
#       if e is event:
#           put it back to front-end db

from utility.event_interface import EventInterface
from utility.base_feature_production import BaseFeatureProduction
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

        self.all_corpus = buildAllCorpus( time_interval_length = 3)
        self.clf = classifier.Classifier() 

    def goThroughCandidateDB(self):
        """Go through candidate event db and classify whatever is left"""
        ei = EventInterface(self.candidate_db, self.candidate_collection)
        ei_classified = EventInterface(self.classified_event_db, self.classified_event_collection)
        #ei_backup = EventInterface(self.event_backup_db, self.event_backup_collection)
        cnt = 0
        
        for e in ei.getAllDocuments():
            print 'working on ',cnt
            e = Event(e)
            cnt+=1
            region = Region(e.getRegion())
            corpus = self.all_corpus[region.getKey()]
            ef = BaseFeatureProduction(e, corpus)     
            prob = self.clf.classify(ef.extractFeatures())

            if ei_classified.getEventByID(e.getID()) is not None:
                if prob>0.5:
                    print 'already in front end collection, merge it'
                    ei_classified.addEvent(e)
                else:
                    print 'after merge it becomes none event, delete it'
                    ei_classified.deleteEventByID(e.getID())
            else:
                if prob>0.5:
                    print 'new events find in collection but not in front end , add it'
                    ei_classified.addEvent(e)
            """
            if prob > 0.5:
                print 'ready to insert'
                e.setLabel( prob )
                tmp_id = "518a755dc2a3750cc221d6fc"
                if ei_classified.getEventByID(tmp_id) is not None:
                    print 'Should merge this event in front end!'
                    print 'before merge photos # ', len(ei.getEventByID(tmp_id)['photos'])
                    ei_classified.addEvent(e)
                    print 'after merge photos  # ', len(ei.getEventByID(tmp_id)['photos'])
                else:
                    print 'not mergeing just add '
                    ei_classified.addEvent(e)
            else:
                if ei_classified.getEventByID()
            """
            #ei_backup.addEvent(e)
            #ei.deleteEventByID(str(e.getID()))
            
    def monitor(self):
        em = EventMonitor('citybeat', 'candidate_event_15by15_merged',  'citybeat', 'instagram_front_end_events', 'citybeat', 'event_backup_instagram')
        while True:
            self.goThroughCandidateDB()
            time.sleep(60)

def test():
    em = EventMonitor('citybeat_production', 'online_candidate_instagram',  'citybeat_production', 'instagram_front_end_events', 'citybeat_production', 'event_backup_instagram')
    em.goThroughCandidateDB()

def main():
    em = EventMonitor('citybeat_production', 'online_candidate_instagram',  'citybeat_production', 'instagram_front_end_events', 'citybeat_production', 'event_backup_instagram')
    while True:
        em.goThroughCandidateDB()
        print 'sleep 3 minutes'
        time.sleep(60*3)

if __name__=='__main__':
    #test()
    main()

