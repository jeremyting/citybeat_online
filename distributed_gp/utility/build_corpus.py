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

def textProprocessor(text):
		
	def removeAt(text):
		# remove @xxx
		new_text = ''
		for word in text.split(' '):
			word = word.strip()
			if word == '':
				continue
			if word.startswith('@'):
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

def getTfidfVector(vectorizer, text):
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

def buildCorpus(region, time_interval, document_type='photos'):
	# time_interval should be [start, end]
	if document_type == 'photos':
		di = PhotoInterface()
	else:
		di = TweetInterface()
	cur = di.rangeQuery(region, time_interval)
	assert cur.count() > 0
	print cur.count()
	text = []
	for document in cur:
		if document_type == 'photos':
			doc = Photo(document)
		else:
			doc = Tweet(document)
		t = doc.getText()
		if len(t) > 1:
			text.append(t)
	
	vectorizer = TfidfVectorizer(max_df=0.05, min_df=0, strip_accents='ascii', preprocessor=textProprocessor,
	                             smooth_idf=True, sublinear_tf=True, norm='l2', 
															 analyzer='word', ngram_range=(1,1), stop_words = 'english')
	vectorizer.fit_transform(text)
	return vectorizer
	
def buildAllCorpus(document_type='photo'):
	assert document_type in ['photo', 'tweet']
	
	all_corpus = {}
	if document_type == 'photo':
		coordinates = [InstagramConfig.photo_min_lat, InstagramConfig.photo_min_lng,
									 InstagramConfig.photo_max_lat, InstagramConfig.photo_max_lng]
	else:
	  coordinates = [TwitterConfig.photo_min_lat, TwitterConfig.photo_min_lng,
									 TwitterConfig.photo_max_lat, TwitterConfig.photo_max_lng]
									 
	nyc = Region(coordinates)
	region_list = nyc.divideRegions(25, 25)
	region_list = nyc.filterRegions(region_list, test=True, n=25, m=25, document_type=document_type)
	now = int(tool.getCurrentStampUTC())
	
	for region in region_list:
		r = Region(region)
		cor = buildCorpus(r, [now - 24 *3600, now], document_type)
		all_corpus[r.toJSON()] = cor

	return all_corpus

if __name__ == '__main__':
	buildAllCorpus('photo')