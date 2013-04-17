import calendar
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
from calendar import timegm

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
    
def textProprocessor(text):
		
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
		
		
if __name__ == "__main__":
    print getCurrentStampUTC()

    print convertTwitterDateToTimestamp("Fri Dec 07 16:12:48 +0001 2012")
