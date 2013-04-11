from mongodb_interface import MongoDBInterface
from element import Element
from region import Region

import operator
import string
import types

class BaseEvent(object):
	
	def __init__(self, event=None, element_type='photo'):
		# the input argument event should be a json, dictionary
		if not event is None:
			if type(event) is types.DictType:
				self._event = event
			else:
				self._event = event.toDict()
				
		if element_type == 'photo':
			self._element_type = 'photos'
		else:
			self._element_type = 'tweets'
				
	def addElement(self, element):
		# element could be a element or tweet
		# when use this method, please keep adding element in chronologically increasing order
		if not type(element) is types.DictType:
			element = element.toDict()
		self._event['elements'].append(element)
		
	def getElementsNumber(self):
		return len(self._event['elements'])
	
	def getLabel(self):
		return self._event['label']
		
	def getActualValue(self):
		return self._event['actual_value']
	
	def _getActualValueByCounting(self):
		# virtual function
		pass
	
	def getRegion(self):
		return self._event['region']
		
	def selectOneElementForOneUser(self):
		# virtual function
		pass
	
	def removeDuplicateElements(self):
		# virtual function
		pass
		
	def containKeywords(self, words, freq=1):
		# virtual function
		pass
	
	def getElementsbyKeyword(self, word):
		# virtual function
		pass
	
	def getZscore(self):
		if 'zscore' in self._event.keys():
			return self._event['zscore']
		else:
			return (float(self._event['actual_value']) - float(self._event['predicted_mu'])) / float(self._event['predicted_std'])
	
	def sortElements(self):
		# this sorting can prevent bugs when merging
		element_list = []
		for element in self._event['elements']:
			element_list.append([element, int(element['created_time']), str(element['id'])])
		element_list.sort(key=operator.itemgetter(1, 2), reverse=True)
		self._event['elements'] = [row[0] for row in element_list]
	
	def mergeWith(self, event):
		if type(event) is types.DictType:
			event = Event(event)
		event = event.toDict()
		
		element_list1 = self._event['elements'] 
		element_list2 = event['elements']
		
		new_element_list = []
		l1 = 0
		l2 = 0
		merged = 0
		while l1 < len(element_list1) and l2 < len(element_list2):
			p1 = Element(element_list1[l1])
			p2 = Element(element_list2[l2])
			compare = p1.compare(p2)
			if compare == 1:
				new_element_list.append(element_list1[l1])
				l1 += 1
				continue
			
			if compare == -1:
				new_element_list.append(element_list2[l2])
				l2 += 1
				merged += 1
				continue
			
			# compare == 0
			new_element_list.append(element_list1[l1])
			l1 += 1
			l2 += 1
		
		while l1 < len(element_list1):
			new_element_list.append(element_list1[l1])
			l1 += 1
		
		while l2 < len(element_list2):
			new_element_list.append(element_list2[l2])
			l2 += 1
			merged += 1
		
		self._event['elements'] = new_element_list
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
	
	def setElements(self, elements):
		# a set of json objects
		self._event['elements'] = elements
		
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
		print self._event['created_time'], 'elements:'
		for element in self._event['elements']:
			print element['created_time']
			
	def getLatestElementTime(self):
		lt = int(self._event['elements'][0]['created_time'])
		for element in self._event['elements']:
			t = int(element['created_time'])
			if t > lt:
				lt = t
		return lt
		
	   
	def getEarliestElementTime(self):
		et = int(self._event['elements'][-1]['created_time'])
		for element in self._event['elements']:
			t = int(element['created_time'])
			if t < et:
				et = t
		return et
		
def main():
	pass