from mongodb_interface import MongoDBInterface
from photo import Photo
from region import Region
from base_event import BaseEvent

import operator
import string
import types

class Event(BaseEvent):
	# Event is for Instagram
	
	def __init__(self, event=None):
		# the input argument event should be a dictionary or python object
		super(Event, self).__init__('photos', event)

				
	def addPhoto(self, photo):
		# when use this method, please keep adding photo in chronologically increasing order
		self.addElement(photo)
		
	def getPhotoNumber(self):
		return self.getElementNumber()
	
		
	def selectOnePhotoForOneUser(self):
		self.leaveOneElementForOneUser()
	
	def removeDuplicatePhotos(self):
		# this method is not good, just for tempory use
		# by judging if the caption is duplicate
		new_photos = []
		num_duplicate = 0
		for photo in self._event['photos']:
			p = Photo(photo)
			is_duplicate = False
			cap1 = p.getCaption()
			user1 = p.getUserName()
			for new_photo in new_photos:
				p2 = Photo(new_photo)
				cap2 = p2.getCaption()
				user2 = p2.getUserName()
				if user1 == user2 and (len(cap1)>0 and cap1 == cap2):
					is_duplicate = True
					num_duplicate += 1
					break
			if not is_duplicate:
				new_photos.append(photo)
				
		if num_duplicate > 0:
			self._event['photos'] = new_photos
			
		return num_duplicate
		
	def containKeywords(self, words, freq=1):
		for word in words:
			res = self.getPhotosbyKeyword(word.lower())
			if len(res) >= freq:
				return True
		return False
	
	def getPhotosbyKeyword(self, word):
		# return a list of photos containg the word
		res_photo = []
		for photo in self._event['photos']:
			cap = Photo(photo).getCaption()
			if cap is None:
				continue
			cap = cap.lower()
			if word in cap:
				res_photo.append(photo)
		return res_photo

	def sortPhotos(self):
		self.sortElements()
	
	def mergeWith(self, event):
		if type(event) is types.DictType:
			event = Event(event)
		event = event.toDict()
		
		photo_list1 = self._event['photos'] 
		photo_list2 = event['photos']
		
		new_photo_list = []
		l1 = 0
		l2 = 0
		merged = 0
		while l1 < len(photo_list1) and l2 < len(photo_list2):
			p1 = Photo(photo_list1[l1])
			p2 = Photo(photo_list2[l2])
			compare = p1.compare(p2)
			if compare == 1:
				new_photo_list.append(photo_list1[l1])
				l1 += 1
				continue
			
			if compare == -1:
				new_photo_list.append(photo_list2[l2])
				l2 += 1
				merged += 1
				continue
			
			# compare == 0
			new_photo_list.append(photo_list1[l1])
			l1 += 1
			l2 += 1
		
		while l1 < len(photo_list1):
			new_photo_list.append(photo_list1[l1])
			l1 += 1
		
		while l2 < len(photo_list2):
			new_photo_list.append(photo_list2[l2])
			l2 += 1
			merged += 1
		
		self._event['photos'] = new_photo_list
		# update actual value
		self.setActualValue(self._getActualValueByCounting())
		
		# do not change the order of the following code
		actual_value_1 = self._event['actual_value']
		actual_value_2  = event['actual_value']
		zscore1 = float(self._event['zscore'])
		zscore2 = float(event['zscore'])
		std1 = float(self._event['predicted_std'])
		std2 = float(event['predicted_std'])
		new_std = (std1 * actual_value_1 + std2 * actual_value_2) / (actual_value_1 + actual_value_2)
		new_zscore = (zscore1 * actual_value_1 + zscore2 * actual_value_2) / (actual_value_1 + actual_value_2)
		self.setZscore(new_zscore)
		new_mu = actual_value_1 - new_zscore * new_std
		self.setPredictedValues(new_mu, new_std)
		
		return merged
				
	def setRegion(self, region):
		if not type(region) is types.DictType:
			region = region.toDict()
		self._event['region'] = region
	
	def setPhotos(self, photos):
		# a set of json objects
		self._event['photos'] = photos
		
	def setCreatedTime(self, utc_time):
		self._event['created_time'] = str(utc_time)
		
	def setPredictedValues(self, mu, std):
		self._event['predicted_mu'] = float(mu)
		self._event['predicted_std'] = float(std)
		
	def setZscore(self, zscore):
		self._event['zscore'] = float(zscore)
		
	def setActualValue(self, actual_value):
		self._event['actual_value'] = int(actual_value)
	
	def setLabel(self, label='unlabeled'):
		self._event['label'] = label
	
	def toDict(self):
		return self._event
		
	def _test_print(self):
		print self._event['created_time'], 'photos:'
		for photo in self._event['photos']:
			print photo['created_time']
			
	def getLatestPhotoTime(self):
		lt = int(self._event['photos'][0]['created_time'])
		for photo in self._event['photos']:
			t = int(photo['created_time'])
			if t > lt:
				lt = t
		return lt
		
	   
	def getEarliestPhotoTime(self):
		et = int(self._event['photos'][-1]['created_time'])
		for photo in self._event['photos']:
			t = int(photo['created_time'])
			if t < et:
				et = t
		return et
		
def main():
	pass