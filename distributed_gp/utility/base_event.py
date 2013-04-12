import operator
import string
import types

class BaseEvent(object):
	
	def __init__(self, element_type, event=None):
		assert element_type in ['photos', 'tweets']
		if element_type == 'photo':
			self._element_type = 'photos'
		else:
			self._element_type = 'tweets'
			
		if not event is None:
			if type(event) is types.DictType:
				self._event = event
			else:
				self._event = event.toDict()
			self.setActualValue(self._getActualValueByCounting())
		else:
			self._event = {}
			self._event[self._element_type] = []	
				
	def addElement(self, element):
		# element could be a element or tweet
		# when use this method, please keep adding element in chronologically increasing order
		if not type(element) is types.DictType:
			element = element.toDict()
		self._event[self._element_type].append(element)
		
	def getElementsNumber(self):
		return len(self._event[self._element_type])
	
	def getLabel(self):
		return self._event['label']
		
	def getActualValue(self):
		return self._event['actual_value']
	
	def _getActualValueByCounting(self):
		# tweet and instagram photos are both ok
		user_ids = set()
		for element in self._event[self._element_type]:
			user_ids.add(int(element['user']['id']))
		return len(user_ids)
	
	def getRegion(self):
		return self._event['region']
		
	def leaveOneElementForOneUser(self):
		# a strong filter
		user_ids = set()
		photos = self._event[self._element_type]
		new_elements = []
		for element in elements:
			user_id = element['user']['id']
			if user_id in user_ids:
				continue
			user_ids.add(user_id)
			new_elements.append(element)
		self._event[self._element_type] = new_elements
	
	def removeDuplicateElements(self):
		# virtual function
		assert 1 == 2
		pass
		
	def containKeywords(self, words, freq=1):
		# virtual function
		assert 1 == 2
		pass
	
	def getElementsbyKeyword(self, word):
		# virtual function
		assert 1 == 2
		pass
	
	def getZscore(self):
		if 'zscore' in self._event.keys():
			return self._event['zscore']
		else:
			return (float(self._event['actual_value']) - float(self._event['predicted_mu'])) / float(self._event['predicted_std'])
	
	def sortElements(self):
		# this sorting can prevent bugs when merging
		element_list = []
		for element in self._event[self._element_type]:
			element_list.append([element, int(element['created_time']), str(element['id'])])
		element_list.sort(key=operator.itemgetter(1, 2), reverse=True)
		self._event[self._element_type] = [row[0] for row in element_list]
	
	def mergeWith(self, event):
		# virtual function
		assert 1 == 2
		pass
				
	def setRegion(self, region):
		if not type(region) is types.DictType:
			region = region.toDict()
		self._event['region'] = region
	
	def setElements(self, elements):
		# a set of json objects
		self._event[self._element_type] = elements
		
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
		for element in self._event[self._element_type]:
			print element['created_time']
			
	def getLatestElementTime(self):
		lt = int(self._event[self._element_type][0]['created_time'])
		for element in self._event[self._element_type]:
			t = int(element['created_time'])
			if t > lt:
				lt = t
		return lt
		
	   
	def getEarliestElementTime(self):
		et = int(self._event[self._element_type][-1]['created_time'])
		for element in self._event[self._element_type]:
			t = int(element['created_time'])
			if t < et:
				et = t
		return et

if __name__ == 'main':
	be = BaseEvent('photo')
	