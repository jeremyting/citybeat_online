import pymongo
from config import db_name
from config import mongo_host
from config import mongo_port
import logging
logging.basicConfig(filename = "/.freespace/instagram_storage.log", level=logging.DEBUG,
format=' [%(asctime)s]   [%(levelname)s] (%(threadName)-10s) %(message)s '
)

def save_mogo(res, mid_lat, mid_lng, db_name):
    mongo = pymongo.Connection(mongo_host, mongo_port)
    mongo_db = mongo[db_name]
    mongo_collection = mongo_db.photos
    print 'trying to save to ',db_name, 'collection = photos'
    for r in res:
        logging.warning("type = "+str(type(r)))
        r['mid_lat'] = mid_lat
        r['mid_lng'] = mid_lng
        r['_id'] = r['id']      #filter dup using instagram internal id
        logging.warning("inserting in to "+db_name+" collection = photos")
        logging.warning("before!")
        mongo_collection.insert(r)
        logging.warning("r = "+str(r))
        logging.warning("after!")
    #mongo.close()
