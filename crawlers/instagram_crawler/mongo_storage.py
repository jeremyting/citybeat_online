import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import pymongo
from utility.photo_interface import PhotoInterface
import logging
logging.basicConfig(filename = "/.freespace/instagram_storage.log", level=logging.DEBUG,
format=' [%(asctime)s]   [%(levelname)s] (%(threadName)-10s) %(message)s '
)

def save_mogo(res, mid_lat, mid_lng):
    photo_interface = PhotoInterface()
    for r in res:
        logging.warning("type = "+str(type(r)))
        r['mid_lat'] = mid_lat
        r['mid_lng'] = mid_lng
        r['_id'] = r['id']      #filter dup using instagram internal id
        logging.warning('inserting photo to mongodb')
        photo_interface.saveDocument(r)
        logging.warning("r = "+str(r))

    #mongo.close()
