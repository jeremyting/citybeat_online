from event_interface import EventInterface
from base_event import BaseEvent
from region import Region
from event import Event
from text_parser import TextParser
from stopwords import Stopwords
from corpus import Corpus
from _kl_divergence import kldiv
from _kl_divergence import tokenize

import kl_divergence as KLDivergence
import tool

import operator
import string
import types
import random
import math
import numpy

class BaseFeature(BaseEvent):
    # this class is the extension of class Event, especially for feature extraction
    # to prevent the class Event from being too long to read
    
    def __init__(self, event, corpus=None, representor=None):
        self._type = tool.getEventType(event)
        self._event = BaseEvent(self._type, event).toDict()
        self._representor = representor
        self._corpus = corpus
    
    def getDuration(self):
        return self.getLatestElementTime() - self.getEarliestElementTime()
    
    def preprocess(self):
        self.selectOneElementForOneUser()
        #self.selectRelaventElements()
    
    def selectRelaventElements(self, k=10):
        assert self._representor is not None
        elements = self._representor.getRepresentiveElements(self.toDict())
        # choose first 30%
#       k = max(k, 0.3*len(elements))
#       k = int(k + 0.5)
        self.setElements(elements[0:min(k, len(elements))])
    
    def countHashtagFromElementContainingTopKeyword(self, k=3):
        # count the number of hashtags of elements that associated with topwords
        # k is the number of top keywords
        # rank top keywords by counting their frequency
        word_element_list = self.getTopKeywordsAndElements(k, 10000)
        cnt = [0]*k
        cnt2 = [0]*k
        for i in xrange(0, len(word_element_list)):
            j = 0
            for element in word_element_list[i][2]:
                p = BaseEvent(self._type, element)
                cap = p.getText()
                j += 1
                cnt[i] += cap.count('#')
            # return the number of hashtags
            cnt[i] = cnt[i] * 1.0 / j
            # reteurn the number of elements
            cnt2[i] = len(word_element_list[i][2])
        return [cnt, cnt2]              
    
    def getTopWordByTFIDF(self, k=3):
        # rank and get the top k words by tfidf
        all_cap = self._getAllTexts()
        tfidf = self._corpus.chooseTopWordWithHighestTDIDF(all_cap, k=3)
        tfidf.sort(reverse=True)
        return tfidf
    
    def _getTopKeywordsWithoutStopwords(self, k):
        # this method will return topwords without stopwords
        return self._getTopWords(k, stopword_removal=True)
        
    def _getRandomElementsAssociatedWithKeywords(self, top_keywords, k=10):
        # get elements associated with the top_keywords
        # k specifies the number of elements to show
        res = []
        for (word, fre) in top_keywords:
            elements = self.getElementsByKeyword(word)
            # this has the shuffling process
            random.shuffle(elements)
            k = min(len(elements), k)
            # discard the keywords with only one element
#           if k == 1:
#               break
            res.append([word, fre, elements[0:k]])
        return res
    
    def getTopKeywordsAndElements(self, num_keywords, num_elements):
        # get top words and its related elements
        keywords = self._getTopKeywordsWithoutStopwords(num_keywords)
        return self._getRandomElementsAssociatedWithKeywords(keywords, num_elements)
    
    def _getElementAvgLocation(self):
        # no use
        elements = self._event[self._element_type]
        lat = 0
        lng = 0
        n = 0
        for element in elements:
            pLat = float(element['location']['latitude'])
            pLon = float(element['location']['longitude'])
            lat += pLat
            lng += pLon
            n += 1      
        return lat/n, lng/n
        
    def _getTopWords(self, k, stopword_removal=False):
        # get top words by counting the frequecy
        text_parser = TextParser(stopword_removal=stopword_removal)
        for element in self._event[self._element_type]:
            p = BaseEvent(self._type, element)
            text = p.getText()
            if not text is None:
                text_parser.insertText(text)
        return text_parser.getTopWords(k)
    
    def extractFeatures(self, entropy_para=3, k_topwords=3):
        # it outputs the feature vector
        self.preprocess()
        avg_cap_len = self.getAvgTextLen()
        dis_feautures = self.getElementDisFeatures()
        std_element_dis = dis_feautures[0]
        avg_element_dis = dis_feautures[1]
        mean_element_dis_cap = self.getElementTextDisFeatures()
        cap_per = self.getTextPercentage()
        std = self.getPredictedStd()
        top_word_pop = self.getTopWordPopularity(k_topwords)
        zscore = self.getZscore()
        entropy = self.getEntropy(entropy_para)
        
        label = int(self.getLabel())
        event_id = str(self._event['_id'])
        
        tfidf_top3 = self.getTopWordByTFIDF(3)
        res = self.countHashtagFromElementContainingTopKeywords(3)
        hashtage_cnt3 = res[0]
        number_elements_associated_with_keywords3 = res[1]
        
#       historic_features = [0]*3   for test only
        historic_features = self.getHistoricFeatures(entropy_para)
        diff_avg_element_dis = avg_element_dis - historic_features[0]
        diff_top_word_pop = historic_features[1]
        diff_entropy = historic_features[2]
        
        location_name_similarity = self.getTopElementsLocationSimilarity()
        
        return [avg_cap_len,
				std_element_dis, avg_element_dis, 
                mean_element_dis_cap,
                cap_per,
                std, top_word_pop, zscore, entropy, #ratio,
                diff_avg_element_dis, diff_top_word_pop, diff_entropy,
                tfidf_top3[0], tfidf_top3[1], tfidf_top3[2], 
                hashtage_cnt3[0], hashtage_cnt3[1], hashtage_cnt3[2],
                number_elements_associated_with_keywords3[0], number_elements_associated_with_keywords3[1], number_elements_associated_with_keywords3[2],
                location_name_similarity, 
                event_id,
                label]
                
    def printFeatures(self):
        feature_list = self.extractFeatures()
        n = len(feature_list)
        for i in xrange(0, n-1):
            print feature_list[i],',',
        print feature_list[-1]
            
            
#   @staticmethod
    def GenerateArffFileHeader(self):
        print '@relation CityBeatEvents'
        print '@attribute AvgTextLen real'
#       print '@attribute stat_MinElementDis real'
#       print '@attribute stat_MaxElementDis real'
        print '@attribute stat_StdElementDis real'
        print '@attribute AvgElementDis real'
#       print '@attribute stat_MedianElementDis real'
#       print '@attribute stat_MinElementDisbyCap real'
#       print '@attribute stat_MaxElementDisbyCap real'
#       print '@attribute stat_StdElementDisbyCap real'
        print '@attribute MeanElementDisbyCap real'
#       print '@attribute stat_MedianElementDisbyCap real'
        print '@attribute TextPercentage real'
        print '@attribute PredictedStd real'
        print '@attribute TopWordPopularity real'
        print '@attribute Zscore real'
        print '@attribute Entropy real'
        print '@attribute diff_AvgElementDis real'
        print '@attribute diff_TopWordPopularity real'
        print '@attribute diff_Entropy real'

        print '@attribute tfidf1 real'  
        print '@attribute tfidf2 real'  
        print '@attribute tfidf3 real'
        
        print '@attribute NumberOfhashtags1 real'   
        print '@attribute NumberOfhashtags2 real'   
        print '@attribute NumberOfhashtags3 real'   
        
        print '@attribute NumberOfPhotsoContaingTopWord1 real'
        print '@attribute NumberOfPhotsoContaingTopWord2 real'
        print '@attribute NumberOfPhotsoContaingTopWord3 real'
        
        print '@attribute Top10ElementLocationNameFreq real'
#       print '@attribute Top3ElementLocationNameSame real'
                                
        print '@attribute ID string'
        print '@attribute label {1,-1}'
        print '@data'
        
    def getElementTextDisFeatures(self):
        # one feauture, compute the average element-to-element textual distance (similarity, KL divergence) 
        
        def ElementDistanceByText(element1, element2):
            
            p1 = BaseEvent(self._type, element1)
            p2 = BaseEvent(self._type, element2)
            cap1 = p1.getText()
            cap2 = p2.getText()
            cp1 = TextParser(True)
            cp1.insertText(cap1)
            cp2 = TextParser(True)
            cp2.insertText(cap2)
            word_list1 = cp1.getTopWords(-1)
            word_list2 = cp2.getTopWords(-1)
            if len(word_list1) == 0 or len(word_list2) == 0:
                # unable to compare
                return None
            word_dict1 = {}
            for word, freq in word_list1:
                word_dict1[word] = freq
            word_dict2 ={}
            for word, freq in word_list2:
                word_dict2[word] = freq
            return kldiv(word_dict1, word_dict2)
            
        elements = self._event[self._element_type]
        diss = []
        for i in xrange(0, len(elements)):
            avgDis = 0
            avail = 0
            for j in xrange(0, len(elements)):
                if i == j:
                    continue
                val = ElementDistanceByText(elements[i], elements[j])
                if val is None:
                    continue
                avail += 1
                avgDis += val
            if avail > 0:
                diss.append(1.0*avgDis / avail)
            else:
                diss.append(10.0)
        return self._computeSimpleStatistic(diss)
    
    
    def _computeGeolocationCenter(self):
        lat = 0
        lon = 0
        for element in self._event[self._element_type]:
            lat += float(element['location']['latitude'])
            lon += float(element['location']['longitude'])
        return lat/len(self._event[self._element_type]), lon/len(self._event[self._element_type])
    
    def _computeSimpleStatistic(self, my_values):
        return [numpy.min(my_values), numpy.max(my_values), numpy.std(my_values),
                numpy.mean(my_values), numpy.median(my_values)] 
    
    def getElementDisFeatures(self):
        #average element-to-element geolocation distance
        
        def elementDistance(element1, element2):
            # inside method, do not call
            lat1 = float(element1['location']['latitude'])
            lon1 = float(element1['location']['longitude'])
            lat2 = float(element2['location']['latitude'])
            lon2 = float(element2['location']['longitude'])
            return math.sqrt(10000*(lat1-lat2)*(lat1-lat2) + 10000*(lon1-lon2)*(lon1-lon2))
            
        elements = self._event[self._element_type]
        n = len(elements)
        # n would be very small when we compute the historical features
        if n < 2:
            return [2.0, 2.0, 0, 2.0, 2.0]
        
        # add three features
        # how much percentage of elements in one sigma
        # how much percentage of elements in two sigma
        # how much percentage of elements in 3 sigma 
        # 3 closest elements are within how many sigma, maybe a good feature
        
        diss = []
        
        for i in xrange(0, n):
            dis_to_other_element = 0
            for j in xrange(0, n):
                if not i == j:
                    pairwiseDis = elementDistance(elements[i], elements[j])
                    dis_to_other_element += pairwiseDis
            dis_to_other_element = dis_to_other_element / (n-1)
            diss.append(dis_to_other_element)
        
        return self._computeSimpleStatistic(diss)
    
    def getAvgTextLen(self):
        # not a good feature
        cap_number = 0
        cap_lens = 0
        elements = self._event[self._element_type]
        for element in elements:
            element = BaseEvent(self._type, element)
            cap_len = len(element.getText())
            if cap_len > 0:
                cap_lens += cap_len
                cap_number += 1
        if cap_number == 0:
            return -1
        else:
            return 1.0 * cap_lens / cap_number
    
    def getTextPercentage(self):
        # not a good feature
        cap_number = 0
        elements = self._event[self._element_type]
        for element in elements:
            element = BaseEvent(self._type, element)
            cap_len = len(element.getText())
            if cap_len > 0:
                cap_number += 1
        return cap_number * 1.0 / len(elements)
    
    def _getAllTexts(self):
        cap = ''
        for element in self._event[self._element_type]:
            cap += BaseEvent(self._type, element).getText() + ' '
        return cap.strip()
    
    def getTopWordPopularity(self, k=1):
        # compute the average popularity of k-top words
        top_words = self._getTopWords(k, True)
        if len(top_words) == 0:
            return 0
        avg_pop = 0
        for top_word in top_words:
            avg_pop += top_word[1]
        return avg_pop / min(k, len(top_words))
    
    def getPredictedStd(self):
        return float(self._event['predicted_std'])
        
    def getPredictedMu(self):
        return float(self._event['predicted_mu'])
        
    def _divideAndCount(self, n):
        # devide the region into n*n grids to compute the entropy
        # p(i) = # of elements in that grid, to the total number of grids
        # it returns the list of subregions associated with the number elements falling into that region
        element_number = self.getElementNumber()
        region = Region(self._event['region'])
        subregions = region.divideRegions(n, n)
        
        # Laplacian smoothed
        pro = [1.0]*n*n
        s = n*n
        elements = self._event[self._element_type]
        for element in elements:
            lat = element['location']['latitude']
            lng = element['location']['longitude']
            flag = False
            i = 0
            for subregion in subregions:
                if subregion.insideRegion([lat, lng]):
                    pro[i] += 1.0
                    s += 1
                    if flag == True:
                        raise Exception('bad data')
                    flag = True
                i += 1
        for i in xrange(0, n*n):
            pro[i] /= s
        return pro
        
        
    def getEntropy(self, n):
        # devide the region into n*m grids to compute the entropy
        # p(i) = # of elements in that grid, to the total number of grids
        pro = self._divideAndCount(n)
        # h(x) = sum(p(x)*log(p(x))
        # Laplacian smoothed
        element_number = self.getElementNumber() + n * n
        h = 0
        for pr in pro:
            h += - math.log(pr)/math.log(2)*pr
        return h
            
    def getRatioOfPeopleToBaseEvent(self):
        # not a good feature
        return 1.0 * self.getActualValue() / len(self._event[self._element_type])
        
    
    def getTopElementsLocationSimilarity(self, k=10):
        freq = {}
        most_freq = 0
        k = min(k, len(self._event[self._element_type]))
        for element in self._event[self._element_type]:
            p = BaseEvent(self._type, element)
            location_name = p.getLocationName()
            if location_name == '':
                    continue
            cur_freq = freq.get(location_name, 0) + 1
            freq[location_name] = cur_freq
            if cur_freq > most_freq:
                most_freq = cur_freq
        return most_freq*1.0 / k
        
    def checkIfTopElementLocationSame(self, k=3):
        k = min(k, len(self._event[self._element_type]))
        elements = self._event[self._element_type]
        location_name = BaseEvent(self._type, elements[0]).getLocationName()
        if location_name == '':
            return 0
        for i in xrange(1, k):
            if not BaseEvent(self._type, elements[i]).getLocationName() == location_name:
                return 0
        return 1
            
    def getHistoricFeatures(self, entropy_para):
        # this method computes the features that capture the difference between current
        # event and background knowledge
        
        end_time = self.getLatestElementTime()
        begin_time = self.getEarliestElementTime()
        if self._element_type == 'photos':
            pi = PhotoInterface()
        else:
            pi = TweetInterface()
        
        elements = []
        dt = 0
        for day in xrange(1,15):
            # here 15 is hard coded because we use 14 days' data as the training
            et = end_time - day * 24 * 3600 + dt / 2
            bt = begin_time - day * 24 * 3600 - dt / 2
            day_elements = pi.rangeQuery(self._event['region'], [str(bt), str(et)])
            for element in day_elements:
                # since rangeQuery sorts the elements from the most current to the most early
                # thus all the elements in the List "elements" are sorted by their created time from 
                # the most current to the most early
                elements.append(element)
                
        random.shuffle(elements)
        elements = elements[0:min(len(self._event[self._element_type]), len(elements))]
        
        if len(elements) == 0:
            # TODO: refine
            return [1, 10, 10]
            
        # fake a historic event
        historic_event = BaseEvent(self._element_type)
        historic_event.setElements(elements)
        historic_event.setRegion(self._event['region'])
        historic_event.setActualValue(historic_event._getActualValueByCounting())
        historic_event = BaseFeature(historic_event)
        
        # compute the difference between entropy
        # this has been smoothed
        pro1 = self._divideAndCount(entropy_para)
        pro2 = historic_event._divideAndCount(entropy_para)
        entropy_divergence = KLDivergence.averageKLDivergence(pro1, pro2)
        
        # compute the difference between top words
        
        topic_divergence = self.computeWordKLDivergenceWith(historic_event)
        
        return [historic_event.getElementDisFeatures()[3], topic_divergence,
#               historic_event.getEntropy(entropy_para),
                entropy_divergence]
    
    def computeWordKLDivergenceWithByEddie(self, event):
        # this method calls the kl divergence computation by eddie's methods
        text1 = ''
        text2 = ''
        for element in self._event[self._element_type]:
            p = BaseEvent(self._type, element)
            text1 += ' '
            text1 += p.getText()
        
        if type(event) is not types.DictType:
            event = event.toDict()
            
        for element in event[self._element_type]:
            p = BaseEvent(self._type, element)
            text2 += ' '
            text2 += p.getText()
        return kldiv(tokenize(text1), tokenize(text2))
    
    def computeWordKLDivergenceWith(self, event):
        if type(event) is types.DictType:
            fake_event = BaseFeature(event)
        else:
            fake_event = event
        event_topword_list = self._getTopWords(-1, True)
        event_topword_list2 = fake_event._getTopWords(-1, True)
        
        n_ind = 0
        ind = {}
        for word, freq in event_topword_list + event_topword_list2:
            if not ind.has_key(word):
                ind[word] = n_ind
                n_ind += 1
        freq1 = [0] * n_ind
        freq2 = [0] * n_ind
        for word, freq in event_topword_list:
            freq1[ind[word]] = freq
        for word, freq in event_topword_list2:
            freq2[ind[word]] = freq
        topic_divergence = KLDivergence.averageKLDivergence(freq1, freq2)
        return topic_divergence
    
            
if __name__=='__main__':
    generateData()