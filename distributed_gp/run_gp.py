import time
import math
import sys

from utility.region import Region
from utility.config import InstagramConfig
from utility.config import TwitterConfig
from rq import Queue, Connection
from redis import Redis
from do_gp import Predict

from gp_job import GaussianProcessJob
from utility.prediction_interface import PredictionInterface
from utility.prediction import Prediction
from utility.tool import getCurrentStampUTC

def save_to_mongo(_results, _saved, model_update_time, data_source):
    done = True
    for key in _results.keys():
        result_pair = _results[key]
        if result_pair[1].return_value is None:
            done = False
            continue
        else:
            if _saved[key] == False:
                _saved[key] = True
                to_save = (result_pair[0], result_pair[1].return_value, result_pair[2]) 
                region = to_save[0]
                for single_hour_prediction in zip(to_save[1], to_save[2]):
                    p = Prediction()
                    p.setRegion(region)
                    p.setModelUpdateTime(model_update_time)
                    p.setPredictedValues( float(single_hour_prediction[0][1]), math.sqrt(float(single_hour_prediction[0][2])))
                    p.setTime( str(single_hour_prediction[1]) )
                    p_json = p.toDict()
                    if data_source == 'twitter':
                        save_interface = PredictionInterface( ) 
                        save_interface.setDB(TwitterConfig.prediction_db)
                        save_interface.setCollection(TwitterConfig.prediction_collection)
                        save_interface.saveDocument( p_json )
                    elif data_source == 'instagram':
                        save_interface = PredictionInterface( ) 
                        save_interface.setDB(InstagramConfig.prediction_db)
                        save_interface.setCollection(InstagramConfig.prediction_collection)
                        save_interface.saveDocument( p_json )

    return done


def run(data_source):
    coordinates = [InstagramConfig.photo_min_lat,
            InstagramConfig.photo_min_lng,
            InstagramConfig.photo_max_lat,
            InstagramConfig.photo_max_lng
                 ]
    nyc_region = Region(coordinates)
    regions = nyc_region.divideRegions(25, 25)
    if data_source == 'twitter':
        regions = nyc_region.filterRegions(regions, test=False, n=25, m=25, document_type='tweet')
    elif data_source == 'instagram':
        regions = nyc_region.filterRegions(regions, test=False, n=25, m=25, document_type='photo')

    #regions = huge_region.divideRegions(25,25)
    #filtered_regions = huge_region.filterRegions( regions )
    #regions = filtered_regions

    for r in regions:
        r.display()

    cur_utc_timestamp = getCurrentStampUTC() 
    
    _results =  {} 
    _saved = {}

    redis_conn = Redis("tall4")
    redis_queue = Queue(connection = redis_conn)
    fourteen_days_ago = cur_utc_timestamp - 24*14*3600

    for i in range(len(regions)):
        test_region = regions[i]
        try:
            gp = GaussianProcessJob( test_region, str(fourteen_days_ago), str(cur_utc_timestamp) , redis_queue)
            res, pred_time = gp.submit()
        except Exception as e:
            print 'Initialization of gp error. continue, error message %s'%(e)
            continue
        _results[gp.getID()] = (test_region, res, pred_time)
        _saved[ gp.getID() ] = False

    save_to_mongo(_results, _saved, cur_utc_timestamp, data_source) 
    done = False
    while not done:
        done = save_to_mongo(_results, _saved, cur_utc_timestamp, data_source)
        time.sleep(10)

    print 'finish work' 
if __name__ == "__main__":
    assert( sys.argv[1] in ['twitter', 'instagram'])
    if sys.argv[1] == 'twitter':
        run(data_source = 'twitter')
    elif argv[1] == 'instagram':
        run(data_source = 'instagram')                            
