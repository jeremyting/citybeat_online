import operator
import types

from region import Region
from photo import Photo
from tweet import Tweet
from base_element import BaseElement


class BaseEvent(object):
    def __init__(self, element_type, event=None):
        assert element_type in ['photos', 'tweets']
        self._element_type = element_type
        if not event is None:
            if type(event) is types.DictType:
                self._event = event
            else:
                self._event = event.toDict()

            r = Region(self._event['region'])
            r._roundTo8Digits()
            self._event['region'] = r.toDict()

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

    def getAllElements(self):
        return self._event[self._element_type]

    def getElementNumber(self):
        return len(self._event[self._element_type])

    def getLabel(self):
        return self._event['label']

    def getID(self):
        return self._event['_id']

    def getActualValue(self):
        return self._event['actual_value']

    def _getActualValueByCounting(self):
        # tweet and instagram elements are both ok
        user_ids = set()
        for element in self._event[self._element_type]:
            user_ids.add(int(element['user']['id']))
        return len(user_ids)

    def getRegion(self):
        # returned is a dictionary
        return self._event['region']

    def leaveOneElementForOneUser(self):
        # a strong filter
        user_ids = set()
        elements = self._event[self._element_type]
        new_elements = []
        for element in elements:
            user_id = element['user']['id']
            if user_id in user_ids:
                continue
            user_ids.add(user_id)
            new_elements.append(element)
        self._event[self._element_type] = new_elements

    def removeDuplicateElements(self):
        new_elements = {}
        for element in self._event[self._element_type]:
            if self._element_type == 'photos':
                d = Photo(element)
            else:
                d = Tweet(element)
            key = d.getText() + '|' + d.getUserId()
            new_elements[key] = d
        self._event[self._element_type] = []
        for key, d in new_elements.items():
            self._event[self._element_type].append(d)
            # need to sort the elements elements or tweets
        self.sortElements()

    def getElementsByKeyword(self, word):
        # return a list of elements containg the word
        res_element = []
        for element in self._event[self._element_type]:
            if self._element_type == 'photos':
                text = Photo(element).getText()
            else:
                text = Tweet(element).getText()
            if word.lower() in text.lower():
                res_element.append(element)
        return res_element

    def getZscore(self):
        if 'zscore' in self._event.keys():
            return self._event['zscore']
        else:
            return (float(self._event['actual_value']) - float(self._event['predicted_mu'])) / float(
                self._event['predicted_std'])

    def sortElements(self):
        # this sorting can prevent bugs when merging
        element_list = []
        for element in self._event[self._element_type]:
            element_list.append([element, int(element['created_time']), str(element['id'])])
        element_list.sort(key=operator.itemgetter(1, 2), reverse=True)
        self._event[self._element_type] = [row[0] for row in element_list]

    def _mergeWith(self, event):

        if type(event) is not types.DictType:
            event = event.toDict()

        element_list1 = self._event[self._element_type]
        element_list2 = event[BaseEvent(self._element_type, event)._element_type]

        new_element_list = []
        l1 = 0
        l2 = 0
        merged = 0
        while l1 < len(element_list1) and l2 < len(element_list2):
            if self._element_type == 'photos':
                d1 = Photo(element_list1[l1])
                d2 = Photo(element_list2[l2])
            else:
                d1 = Tweet(element_list1[l1])
                d2 = Tweet(element_list2[l2])
            compare = d1.compare(d2)
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

        self._event[self._element_type] = new_element_list
        # update actual value
        self.setActualValue(self._getActualValueByCounting())

        # do not change the order of the following code
        actual_value_1 = self._event['actual_value']
        actual_value_2 = event['actual_value']
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
        # a set of dictionaries
        assert type(elements[0]) is types.DictType
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

    def getGeoLocationCenter(self):
        lat = 0
        lon = 0
        n = len(self._event[self._element_type])
        for element in self._event[self._element_type]:
            element = BaseElement(element)
            loc = element.getLocations()
            lat += loc[0]
            lon += loc[1]
        return [lat / n, lon / n]


if __name__ == 'main':
    be = BaseEvent('photos')
    