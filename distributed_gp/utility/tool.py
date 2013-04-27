import calendar
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
from calendar import timegm
import types

def getCurrentStampUTC():
    cur_utc_timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
    return cur_utc_timestamp

def convertTwitterDateToTimestamp(time_string):
    dt = int(mktime_tz(parsedate_tz(ts.strip())))
    return dt
    
def processAsPeopleCount(data):
    # process the data and delete those that are "floodingly" upload photos
    # eliminate photos that are within a time window
    user_last_upload = {}
    return_data = []
    window_size = 600
    for photo_json in data:
        user = photo_json['user']['username']
        if user not in user_last_upload:
            user_last_upload[user] = int(photo_json['created_time'])
            return_data.append(photo_json)
        else:
            if float(photo_json['created_time']) - float(user_last_upload[user]) > window_size: 
                user_last_upload[user] = int(photo_json['created_time'])
            else:
                return_data.append(photo_json)
    return return_data
    
def textPreprocessor(text):   
    def removeAt(text):
        # remove @xxx
        new_text = ''
        for word in text.split(' '):
            word = word.strip()
            if word == '' or word.startswith('@'):
                continue
            new_text += word + ' '
        return new_text.strip()
        
    text = removeAt(text)
    # change the word YouLoveMe into you love me seperately
    new_text = ''
    pre_is_text = False
    for c in text:
        if c.isupper():
            if not pre_is_text:
                new_text += ' '
            new_text += c.lower()
            pre_is_text = True
            continue
        if c.islower():
            new_text += c
        else:
            new_text += ' '
        pre_is_text = False
    new_text = removeAt(new_text)
    return new_text.strip()


def getAllActualEvents():
    
    ei = EventInterface()
    ei.setDB('citybeat')
    ei.setCollection('candidate_event_25by25_merged')
    
    true_events = []
    false_events = []
    fid2 = open('labeled_data_cf/181_positive.txt', 'r')
        
    modified_events = {}
    
    for line in fid2:
        t = line.split(',')
        modified_events[str(t[0])] = int(t[1])
    fid2.close()
        
    # put the data into a text file first
    fid = open('labeled_data_cf/data2.txt','r')
    for line in fid:
        if len(line.strip()) == 0:
            continue
        t = line.strip().split()
        if not len(t) == 3:
            continue
        label = t[0].lower()
        confidence = float(t[1])
        event_id = str(t[2].split('/')[-1])
        if label == 'not_sure':
            continue
        if label == 'yes':
            label = 1
        else:
            label = -1
        event = ei.getDocument({'_id':ObjectId(event_id)})
        event['label'] = label
        if modified_events.has_key(event_id):
            event['label'] = modified_events[event_id]
        
        e = Event(event)
        if e.getActualValue() < 8 or event['label'] == 0:
#           print 'bad event ' + id
            continue
        if event['label'] == 1:
            true_events.append(event)
            
    fid.close()
    return true_events

def getEventType(event):
    if type(event) is types.DictType:
        if 'tweets' in event.keys():
            return 'tweets'
        if 'photos' in event.keys():
            return 'photos'
    else:
        return event._element_type
    
		

        
if __name__ == "__main__":
    print getCurrentStampUTC()

    print convertTwitterDateToTimestamp("Fri Dec 07 16:12:48 +0001 2012")
