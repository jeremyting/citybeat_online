from utility.event_interface import EventInterface


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