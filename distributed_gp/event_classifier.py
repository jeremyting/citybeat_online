"""
Procedure is as follow:
read tf-idf
 while
   search db
   if e not classified
       classify e.
       if e is event:
           put it back to front-end db
"""
import logging
import time

import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.event_interface import EventInterface
from utility.base_feature_production import BaseFeatureProduction
from utility.corpus import buildAllCorpus
from utility.region import Region
from utility.event import Event
from utility.tool import getCurrentStampUTC
import classifier


class EventMonitor():
    def __init__(self, candidate_db, candidate_collection, classified_event_db, classified_event_collection,
                 event_backup_db, event_backup_collection):
        self.candidate_db = candidate_db
        self.candidate_collection = candidate_collection
        self.classified_event_db = classified_event_db
        self.classified_event_collection = classified_event_collection
        self.event_backup_db = event_backup_db
        self.event_backup_collection = event_backup_collection
        # here we have a problem, if there is no photo during that period, need to provide a empty vector
        self.all_corpus = buildAllCorpus(time_interval_length=3)
        self.clf = classifier.Classifier()

    def goThroughCandidateDB(self):
        """Go through candidate event db and classify whatever is left"""
        ei = EventInterface(self.candidate_db, self.candidate_collection)
        ei_classified = EventInterface(self.classified_event_db, self.classified_event_collection)
        cnt = 0
        # consider past 2 hours for merge
        low_bound = str(int(getCurrentStampUTC()) - 60 * 60 * 2)
        condition = {'created_time':{ '$gte':  low_bound}}
        for e in ei.getAllDocuments(condition=condition):
            logging.warning("Classifying %d-th candidate event..." % cnt)
            e = Event(e)
            cnt += 1
            region = Region(e.getRegion())
            corpus = self.all_corpus[region.getKey()]
            ef = BaseFeatureProduction(e, corpus)
            prob = self.clf.classify(ef.extractFeatures())

            if ei_classified.getEventByID(e.getID()) is not None:
                if prob > 0.5:
                    print 'already in front end collection, merge it'
                    ei_classified.addEvent(e)
                else:
                    print 'after merge it becomes none event, delete it'
                    ei_classified.deleteEventByID(e.getID())
            else:
                if prob > 0.5:
                    print 'new events find in collection but not in front end , add it'
                    ei_classified.addEvent(e)

            # ei.deleteEventByID(str(e.getID()))

def main():
    em = EventMonitor('citybeat_production', 'online_candidate_instagram', 'citybeat_production',
                      'instagram_front_end_events', 'citybeat_production', 'event_backup_instagram')
    while True:
        em.goThroughCandidateDB()
        print 'sleep 3 minutes'
        time.sleep(60 * 3)


if __name__ == '__main__':
    main()

