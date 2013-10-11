import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import production_back_end_db
from utility.config import StatsConfig

class _BaseStatsInterface(MongoDBInterface):

    def __init__(self, db_name=production_back_end_db, collection_name=None):
        assert collection_name in [StatsConfig.instagram_collection, StatsConfig.twitter_collection]
        super(_BaseStatsInterface, self).__init__()
        self.setDB(db_name)
        self.setCollection(collection_name)

class InstagramStatsInterface(_BaseStatsInterface):

    def __init__(self):
        super(InstagramStatsInterface, self).__init__(collection_name=StatsConfig.instagram_collection)

class TwitterStatsInterface(_BaseStatsInterface):

    def __init__(self):
        super(TwitterStatsInterface, self).__init__(collection_name=StatsConfig.twitter_collection)