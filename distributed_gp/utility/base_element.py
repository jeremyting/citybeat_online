import types


class BaseElement(object):
	
	def __init__(self, element):
		if type(element) is types.DictType:
			self._element = element
		else:
			self._element = element.toDict()
	
	def getLocationName(self):
		# virtual function
		assert 1 == 2
		pass
		
	def getUserId(self):
		return str(self._element['user']['id'])
	
	def getLocations(self):
		lat = float(self._element['location']['latitude'])
		lon = float(self._element['location']['longitude'])
		return [lat, lon]
	
	def toDict(self):
		return self._element
	
	def equalWith(self, element):
		return self.compare(element) == 0
	
	def compare(self, element):
		if not type(element) is types.DictType:
			element = element.toDict()
		t1 = int(self._element['created_time'])
		t2 = int(element['created_time'])
		id1 = str(self._element['id'])
		id2 = str(element['id'])
		
		if t1 > t2:
			return 1
		if t1 < t2:
			return -1
		if id1 > id2:
			return 1
		if id1 < id2:
			return -1
		return 0
