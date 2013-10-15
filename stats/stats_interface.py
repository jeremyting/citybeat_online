import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import production_back_end_db
from utility.config import StatsConfig

class StatsInterface(MongoDBInterface):

    def __init__(self, db_name=production_back_end_db, collection_name=StatsConfig.collection):
        super(StatsInterface, self).__init__()
        self.setDB(db_name)
        self.setCollection(collection_name)