from event_interface import EventInterface
from caption_parser import CaptionParser
from photo import Photo

from photo_interface import PhotoInterface
from tweet_interface import TweetInterface
from photo import Photo
from tweet import Tweet
from region import Region
from config import InstagramConfig
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import tool

import random
import time
from datetime import datetime


import time
import math
import operator

class Corpus(object):
	
	def getKey(self):
		assert self._region not is None
		r = Region(self._region)
		return r.toJSON()
		
	def _textProprocessor(text):
		
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
		
	def buildCorpus(region, time_interval, document_type='photo'):
		# time_interval should be [start, end]
		if document_type == 'photo':
			di = PhotoInterface()
		else:
			di = TweetInterface()
		cur = di.rangeQuery(region, time_interval)
		text = []
		for document in cur:
			if document_type == 'photo':
				doc = Photo(document)
			else:
				doc = Tweet(document)
			t = doc.getText()
			#at least 5 length
			if len(t) > 4:
				text.append(t)
		self._region = region
		self._vectorizer = TfidfVectorizer(max_df=100, min_df=0, strip_accents='ascii', preprocessor=self._textProprocessor,
		                             smooth_idf=True, sublinear_tf=True, norm='l2', 
																 analyzer='word', ngram_range=(1,1), stop_words = 'english')
		self._vectorizer.fit_transform(text)
			
	def chooseTopWordWithHighestTDIDF(self, text, k=10):
			voc = vectorizer.get_feature_names()
			tf_vec = vectorizer.transform([text]).mean(axis=0)
			nonzeros = np.nonzero(tf_vec)[1]
	res_list = nonzeros.ravel().tolist()[0] 
	values = []
	words = []
	for n in res_list:
		words.append( voc[n] )
		values.append( tf_vec[0,n] )
	return res_list, words, values
			
	
if __name__ == '__main__':
	pass