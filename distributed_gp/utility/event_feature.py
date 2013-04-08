from event_interface import EventInterface
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from caption_parser import CaptionParser
from stopwords import Stopwords
from corpus import Corpus
from _kl_divergence import kldiv
from _kl_divergence import tokenize

import kl_divergence as KLDivergence

import operator
import string
import types
import random
import math
import numpy

class EventFeature(Event):
	# this class is the extension of class Event, especially for feature extraction
	# to prevent the class Event from being too long to read
	
	def __init__(self, event, corpus=None, representor=None):
		super(EventFeature, self).__init__(event)
		# note that, if you want to use any feature related with tfidf, corpus must be set
		# the the definition of Corpus class in corpus.py
		if corpus is not None:
			self._corpus = corpus
		if representor is not None:
			self._representor = representor
				
	def getDuration(self):
		return self.getLatestPhotoTime() - self.getEarliestPhotoTime()
	
	
	def preprocess(self):
		self.selectOnePhotoForOneUser()
		self.selectRelaventPhotos()
	
	def selectRelaventPhotos(self, k=10):
		assert self._representor is not None
		photos = self._representor.getRepresentivePhotos(self.toJSON())
		# choose first 30%
#		k = max(k, 0.3*len(photos))
#		k = int(k + 0.5)
		self.setPhotos(photos[0:min(k, len(photos))])
	
	def countHashtagsFromPhotosContainingTopKeywords(self, k=3):
		# count the number of hashtags of photos that associated with topwords
		# k is the number of top keywords
		# rank top keywords by counting their frequency
		word_photo_list = self.getTopKeywordsAndPhotos(k, 10000)
		cnt = [0]*k
		cnt2 = [0]*k
		for i in xrange(0, len(word_photo_list)):
			j = 0
			for photo in word_photo_list[i][2]:
				p = Photo(photo)
				cap = p.getCaption()
				j += 1
				cnt[i] += cap.count('#')
			# return the number of hashtags
			cnt[i] = cnt[i] * 1.0 / j
			# reteurn the number of photos
			cnt2[i] = len(word_photo_list[i][2])
		return [cnt, cnt2]				
	
	def getTopWordByTFIDF(self, k=3):
		# rank and get the top k words by tfidf
		word_list = self._getTopWords(-1, True)
		word_list_tfidf = self._corpus.chooseTopWordWithHighestTDIDF(word_list, k=3)
		freq = [0]*k
		for i in xrange(0, len(word_list_tfidf)):
			freq[i] = word_list_tfidf[i][1]
		return freq
	
	def _getTopKeywordsWithoutStopwords(self, k):
		# this method will return topwords without stopwords
		return self._getTopWords(k, stopword_removal=True)
		
	def _getRandomPhotosAssociatedWithKeywords(self, top_keywords, k=10):
		# get photos associated with the top_keywords
		# k specifies the number of photos to show
		res = []
		for (word, fre) in top_keywords:
			photos = self.getPhotosbyKeyword(word)
			# this has the shuffling process
			random.shuffle(photos)
			k = min(len(photos), k)
			# discard the keywords with only one photo
#			if k == 1:
#				break
			res.append([word, fre, photos[0:k]])
		return res
	
	def getTopKeywordsAndPhotos(self, num_keywords, num_photos):
		# get top words and its related photos
		keywords = self._getTopKeywordsWithoutStopwords(num_keywords)
		return self._getRandomPhotosAssociatedWithKeywords(keywords, num_photos)
	
	def _getPhotoAvgLocation(self):
		# no use
		photos = self._event['photos']
		lat = 0
		lng = 0
		n = 0
		for photo in photos:
			pLat = float(photo['location']['latitude'])
			pLon = float(photo['location']['longitude'])
			lat += pLat
			lng += pLon
			n += 1		
		return lat/n, lng/n
		
	def _getTopWords(self, k, stopword_removal=False):
		# get top words by counting the frequecy
		caption_parser = CaptionParser(stopword_removal=stopword_removal)
		for photo in self._event['photos']:
			p = Photo(photo)
			caption = p.getCaption()
			if not caption is None:
				caption_parser.insertCaption(caption)
		return caption_parser.getTopWords(k)
	
	def extractFeatures(self, entropy_para=3, k_topwords=3):
		# it outputs the feature vector
		self.preprocess()
		avg_cap_len = self.getAvgCaptionLen()
		dis_feautures = self.getPhotoDisFeatures()
		min_photo_dis = dis_feautures[0]
		max_photo_dis = dis_feautures[1]
		std_photo_dis = dis_feautures[2]
		avg_photo_dis = dis_feautures[3]
		median_photo_dis = dis_feautures[4]
		cap_dis_features = self.getPhotoCaptionDisFeatures()
		min_photo_dis_cap = cap_dis_features[0]
		max_photo_dis_cap = cap_dis_features[1]
		std_photo_dis_cap = cap_dis_features[2]
		mean_photo_dis_cap = cap_dis_features[3]
		median_photo_dis_cap = cap_dis_features[4]
		cap_per = self.getCaptionPercentage()
		std = self.getPredictedStd()
		top_word_pop = self.getTopWordPopularity(k_topwords)
		zscore = self.getZscore()
		entropy = self.getEntropy(entropy_para)
		
		label = int(self.getLabel())
		event_id = str(self._event['_id'])
		
		tfidf_top3 = self.getTopWordByTFIDF(3)
		res = self.countHashtagsFromPhotosContainingTopKeywords(3)
		hashtag_cnt3 = res[0]
		number_photos_associated_with_keywords3 = res[1]
		
		
		
#		historic_features = [0]*3  # for test only
		historic_features = self.getHistoricFeatures(entropy_para)
		diff_avg_photo_dis = avg_photo_dis - historic_features[0]
		diff_top_word_pop = historic_features[1]
		diff_entropy = historic_features[2]
		
		location_name_similarity = self.getTopPhotosLocationSimilarity()
#		location_name_same = self.checkIfTopPhotoLocationSame()
		
		return [avg_cap_len,
		        min_photo_dis, max_photo_dis, std_photo_dis, avg_photo_dis, median_photo_dis,
		        min_photo_dis_cap, max_photo_dis_cap,	std_photo_dis_cap,
		        mean_photo_dis_cap, median_photo_dis_cap,
		        cap_per,
		        std, top_word_pop, zscore, entropy, #ratio,
		        diff_avg_photo_dis, diff_top_word_pop, diff_entropy,
		        tfidf_top3[0], tfidf_top3[1], tfidf_top3[2], 
		        hashtag_cnt3[0], hashtag_cnt3[1], hashtag_cnt3[2],
		        number_photos_associated_with_keywords3[0], number_photos_associated_with_keywords3[1], number_photos_associated_with_keywords3[2],
		        location_name_similarity, 
#		        location_name_same,
		        event_id,
		        label]
		        
	def printFeatures(self):
		feature_list = self.extractFeatures()
		n = len(feature_list)
		for i in xrange(0, n-1):
			print feature_list[i],',',
		print feature_list[-1]
			
			
#	@staticmethod
	def GenerateArffFileHeader(self):
		print '@relation CityBeatEvents'
		print '@attribute AvgCaptionLen real'
		print '@attribute stat_MinPhotoDis real'
		print '@attribute stat_MaxPhotoDis real'
		print '@attribute stat_StdPhotoDis real'
		print '@attribute AvgPhotoDis real'
		print '@attribute stat_MedianPhotoDis real'
		print '@attribute stat_MinPhotoDisbyCap real'
		print '@attribute stat_MaxPhotoDisbyCap real'
		print '@attribute stat_StdPhotoDisbyCap real'
		print '@attribute MeanPhotoDisbyCap real'
		print '@attribute stat_MedianPhotoDisbyCap real'
		print '@attribute CaptionPercentage real'
		print '@attribute PredictedStd real'
		print '@attribute TopWordPopularity real'
		print '@attribute Zscore real'
		print '@attribute Entropy real'
		print '@attribute diff_AvgPhotoDis real'
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
		
		print '@attribute Top10PhotoLocationNameFreq real'
#		print '@attribute Top3PhotoLocationNameSame real'
								
		print '@attribute ID string'
		print '@attribute label {1,-1}'
		print '@data'
		
	def getPhotoCaptionDisFeatures(self):
		# one feauture, compute the average photo-to-photo textual distance (similarity, KL divergence) 
		
		def PhotoDistanceByCaption(photo1, photo2):
			
			p1 = Photo(photo1)
			p2 = Photo(photo2)
			cap1 = p1.getCaption()
			cap2 = p2.getCaption()
			cp1 = CaptionParser(True)
			cp1.insertCaption(cap1)
			cp2 = CaptionParser(True)
			cp2.insertCaption(cap2)
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
			
		photos = self._event['photos']
		diss = []
		for i in xrange(0, len(photos)):
			avgDis = 0
			avail = 0
			for j in xrange(0, len(photos)):
				if i == j:
					continue
				val = PhotoDistanceByCaption(photos[i], photos[j])
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
		for photo in self._event['photos']:
			lat += float(photo['location']['latitude'])
			lon += float(photo['location']['longitude'])
		return lat/len(self._event['photos']), lon/len(self._event['photos'])
	
	def _computeSimpleStatistic(self, my_values):
		return [numpy.min(my_values), numpy.max(my_values), numpy.std(my_values),
		        numpy.mean(my_values), numpy.median(my_values)]	
	
	def getPhotoDisFeatures(self):
		#average photo-to-photo geolocation distance
		
		def photoDistance(photo1, photo2):
			# inside method, do not call
			lat1 = float(photo1['location']['latitude'])
			lon1 = float(photo1['location']['longitude'])
			lat2 = float(photo2['location']['latitude'])
			lon2 = float(photo2['location']['longitude'])
			return math.sqrt(10000*(lat1-lat2)*(lat1-lat2) + 10000*(lon1-lon2)*(lon1-lon2))
			
		photos = self._event['photos']
		n = len(photos)
		# n would be very small when we compute the historical features
		if n < 2:
			return [2.0, 2.0, 0, 2.0, 2.0]
		
		# add three features
		# how much percentage of photos in one sigma
		# how much percentage of photos in two sigma
		# how much percentage of photos in 3 sigma 
		# 3 closest photos are within how many sigma, maybe a good feature
		
		
		diss = []
		
		for i in xrange(0, n):
			dis_to_other_photo = 0
			for j in xrange(0, n):
				if not i == j:
					pairwiseDis = photoDistance(photos[i], photos[j])
					dis_to_other_photo += pairwiseDis
			dis_to_other_photo = dis_to_other_photo / (n-1)
			diss.append(dis_to_other_photo)
		
		return self._computeSimpleStatistic(diss)
	
	def getAvgCaptionLen(self):
		# not a good feature
		cap_number = 0
		cap_lens = 0
		photos = self._event['photos']
		for photo in photos:
			photo = Photo(photo)
			cap_len = len(photo.getCaption())
			if cap_len > 0:
				cap_lens += cap_len
				cap_number += 1
		if cap_number == 0:
			return -1
		else:
			return 1.0 * cap_lens / cap_number
	
	def getCaptionPercentage(self):
		# not a good feature
		cap_number = 0
		photos = self._event['photos']
		for photo in photos:
			photo = Photo(photo)
			cap_len = len(photo.getCaption())
			if cap_len > 0:
				cap_number += 1
		return cap_number * 1.0 / len(photos)
		
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
		# p(i) = # of photos in that grid, to the total number of grids
		# it returns the list of subregions associated with the number photos falling into that region
		photo_number = self.getPhotoNumber()
		region = Region(self._event['region'])
		subregions = region.divideRegions(n, n)
		
		# Laplacian smoothed
		pro = [1.0]*n*n
		s = n*n
		photos = self._event['photos']
		for photo in photos:
			lat = photo['location']['latitude']
			lng = photo['location']['longitude']
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
		# p(i) = # of photos in that grid, to the total number of grids
		pro = self._divideAndCount(n)
		# h(x) = sum(p(x)*log(p(x))
		# Laplacian smoothed
		photo_number = self.getPhotoNumber() + n * n
		h = 0
		for pr in pro:
			h += - math.log(pr)/math.log(2)*pr
		return h
			
	def getRatioOfPeopleToPhoto(self):
		# not a good feature
		return 1.0 * self.getActualValue() / len(self._event['photos'])
		
	
	def getTopPhotosLocationSimilarity(self, k=10):
		freq = {}
		most_freq = 0
		k = min(k, len(self._event['photos']))
		for photo in self._event['photos']:
			p = Photo(photo)
			location_name = p.getLocationName()
			if location_name == '':
					continue
			cur_freq = freq.get(location_name, 0) + 1
			freq[location_name] = cur_freq
			if cur_freq > most_freq:
				most_freq = cur_freq
		return most_freq*1.0 / k
		
	def checkIfTopPhotoLocationSame(self, k=3):
		k = min(k, len(self._event['photos']))
		photos = self._event['photos']
		location_name = Photo(photos[0]).getLocationName()
		if location_name == '':
			return 0
		for i in xrange(1, k):
			if not Photo(photos[i]).getLocationName() == location_name:
				return 0
		return 1
			
	def getHistoricFeatures(self, entropy_para):
		# this method computes the features that capture the difference between current
		# event and background knowledge
		
		end_time = self.getLatestPhotoTime()
		begin_time = self.getEarliestPhotoTime()
		
		pi = PhotoInterface()
		pi.setDB('citybeat')
		pi.setCollection('photos')
		
		photos = []
		dt = 0
		for day in xrange(1,15):
			# here 15 is hard coded because we use 14 days' data as the training
			et = end_time - day * 24 * 3600 + dt / 2
			bt = begin_time - day * 24 * 3600 - dt / 2
			day_photos = pi.rangeQuery(self._event['region'], [str(bt), str(et)])
			for photo in day_photos:
				# since rangeQuery sorts the photos from the most current to the most early
				# thus all the photos in the List "photos" are sorted by their created time from 
				# the most current to the most early
				photos.append(photo)
				
		random.shuffle(photos)
		photos = photos[0:min(len(self._event['photos']), len(photos))]
		
		# fake a historic event
		historic_event = Event()
		historic_event.setPhotos(photos)
		historic_event.setRegion(self._event['region'])
		historic_event.setActualValue(historic_event._getActualValueByCounting())
		historic_event = EventFeature(historic_event)
		
		# compute the difference between entropy
		# this has been smoothed
		pro1 = self._divideAndCount(entropy_para)
		pro2 = historic_event._divideAndCount(entropy_para)
		entropy_divergence = KLDivergence.averageKLDivergence(pro1, pro2)
		
		# compute the difference between top words
		
		topic_divergence = self.computeWordKLDivergenceWith(historic_event)
		
		return [historic_event.getPhotoDisFeatures()[3], topic_divergence,
#		        historic_event.getEntropy(entropy_para),
		        entropy_divergence]
	
	def computeWordKLDivergenceWithByEddie(self, event):
		# this method calls the kl divergence computation by eddie's methods
		text1 = ''
		text2 = ''
		for photo in self._event['photos']:
			p = Photo(photo)
			text1 += ' '
			text1 += p.getCaption()
		
		if type(event) is types.DictType:
			pass
		else:
			event = event.toJSON()
			
		for photo in event['photos']:
			p = Photo(photo)
			text2 += ' '
			text2 += p.getCaption()
		return kldiv(tokenize(text1), tokenize(text2))
	
	def computeWordKLDivergenceWith(self, event):
		if type(event) is types.DictType:
			fake_event = EventFeature(event)
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
#	ei = EventInterface()
#	ei.setDB('historic_alarm')
#	ei.setCollection('labeled_event')
#	event = ei.getDocument()
#	e = EventFeature(event)
#	e.getHistoricFeatures()