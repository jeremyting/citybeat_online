import pymongo


source_mongodb_address = 'tall2.rutgers.edu'
source_mongodb_port = 27017
source_connection = pymongo.Connection(source_mongodb_address, source_mongodb_port)

target_mongodb_address = 'grande.rutgers.edu'
target_mongodb_port = 27017
target_connection = pymongo.Connection(target_mongodb_address, target_mongodb_port)

for db in source_connection.database_names():
    print db
    target_connection.copy_database(db, db, source_mongodb_address)
    print 'finished'


