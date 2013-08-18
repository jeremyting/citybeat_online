from base_feature_sparse import BaseFeatureSparse
from utility.photo_interface import PhotoInterface


def transferPhoto():
    # remove duplicate
    pi = PhotoInterface()
    pi.setDB('tmp_citybeat')
    pi.setCollection('photos')

    pi2 = PhotoInterface()
    pi2.setDB('citybeat_production')
    pi2.setCollection('photos')

    photo_cur = pi.getAllDocuments()
    id_set = set()
    for photo in photo_cur:
        if photo['id'] not in id_set:
            id_set.add(photo['id'])
            photo['_id'] = photo['id']
            pi2.saveDocument(photo)

    print len(id_set)


if __name__ == '__main__':
    transferPhoto()
    
    
    
    
    
    
    
    