import pymongo


source_mongodb_address = 'grande.rutgers.edu'
source_mongodb_port = 27017
source_connection = pymongo.Connection(source_mongodb_address, source_mongodb_port)

target_mongodb_address = 'ec2-23-22-67-45.compute-1.amazonaws.com'
target_mongodb_port = 27017
target_connection = pymongo.Connection(target_mongodb_address, target_mongodb_port)

print target_connection.database_names()

'''
target_connection['admin'].authenticate( 'admin', 'mediumdatarules')
try:
    target_connection.copy_database('citybeat_production', 'citybeat_production', source_mongodb_address)
except Exception as e:
    print e
'''
print target_connection.database_names()



