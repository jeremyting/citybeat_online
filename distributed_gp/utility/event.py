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
		self.removeDuplicateElements()
		
	def containKeywords(self, words, freq=1):
		for word in words:
			res = self.getPhotosbyKeyword(word.lower())
			if len(res) >= freq:
				return True
		return False
	
	def getPhotosbyKeyword(self, word):
		return self.getElementsByKeyword(word)

	def sortPhotos(self):
		self.sortElements()
				
	def setPhotos(self, photos):
		self.setElements(photos)
			
	def getLatestPhotoTime(self):
		return self.getLatestElementTime()
	   
	def getEarliestPhotoTime(self):
		return self.getEarliestElementTime()
		
def main():
	pass