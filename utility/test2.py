from bson.objectid import ObjectId

from event_interface import EventInterface
from photo_interface import PhotoInterface


def insertEvents():
    ei = EventInterface()
    ei.setDB('citybeat')
    ei.setCollection('candidate_event_25by25_merged')

    ei2 = EventInterface()
    ei2.setDB('citybeat')
    ei2.setCollection('online_candidate')

    ids = ['51148288c2a3754cfe668edd', '51147952c2a3754cfe6684ee',
           '51148a7ec2a3754cfe669977', '51147967c2a3754cfe668503']

    for id in ids:
        event = ei.getDocument({'_id': ObjectId(id)})
        ei2.addEvent(event)


def findPhotos():
    pi = PhotoInterface()
    pi.setDB('')
    pi.setCollection('')


if __name__ == '__main__':
    pass
#   insertEvents()

