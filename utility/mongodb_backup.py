import pymongo
from mongodb_interface import MongoDBInterface

source_mongodb_address = 'ec2-23-22-67-45.compute-1.amazonaws.com'
source_mongodb_port = 27017
source_connection = pymongo.Connection(source_mongodb_address, source_mongodb_port)
source_connection['admin'].authenticate( 'admin', 'mediumdatarules')

target_mongodb_address = 'grande.rutgers.edu'
target_mongodb_port = 27017
target_connection = pymongo.Connection(target_mongodb_address, target_mongodb_port)

print source_connection.database_names()
print source_connection['citybeat_production'].collection_names()
print target_connection['citybeat_production'].collection_names()


for collection in source_connection['citybeat_production'].collection_names():
    print 'start collection: ' + collection
    source_interface = MongoDBInterface()
    source_interface._connection = source_connection
    source_interface.setDB('citybeat_production')
    source_interface.setCollection(collection)

    target_interface = MongoDBInterface()
    target_interface._connection = target_connection
    target_interface.setDB('citybeat_production')
    target_interface.setCollection(collection)

    count = 0
    for e in source_interface.getAllDocuments():
        try:
            target_interface.saveDocument(e)
            count += 1
        except Exception:
            print 'fail'
    print 'finish collection: ' + collection
    print 'new documents:' + str(count)
print 'finished all'
'''
try:
    source_connection.copy_database('citybeat_production', 'citybeat_production', source_mongodb_address)
except Exception as e:
    print e

print target_connection.database_names()
'''


