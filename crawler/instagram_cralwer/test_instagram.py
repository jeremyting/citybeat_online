""" one and off script to check instagram server status

"""

from instagram import InstagramAPI
import config
import time
from httplib2 import Http
clients = open('clients_list.csv').readlines()

count = 0
for line in clients:
    t = line.split()
    client = InstagramAPI( t[0], t[1])
    try:
        result = client.media_search(lat = 39.92, lng = 116.38 ,count=50, return_json = True )
        print result
    except Exception as e:
        print e
        print 'bad ',count
    count+=1
    break
    
print time.time()
40.763381,-73.954639
