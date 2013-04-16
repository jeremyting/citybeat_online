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


def buildCorpus(region, time_interval, document_type='photos'):
	# time_interval should be [start, end]
	if document_type == 'photos':
		di = PhotoInterface()
	else:
		di = TweetInterface()
	cur = di.rangeQuery(region, time_interval)
	text = []
	for document in cur:
		if document_type == 'photos':
			doc = Photo(document)
		else:
			doc = Tweet(document)
		text.append(doc.getText())
	
	vectorizer = TfidfVectorizer(max_df=0.99, min_df=0, strip_accents='ascii',
	                             smooth_idf=True, sublinear_tf=True, norm='l2', 
															 analyzer='word', ngram_range=(1,1), stop_words = 'english')
	vectorizer.fit_transform(text)
	print vectorizer.transform(text[0])
	return vectorizer



if __name__ == '__main__':
	coordinates = [InstagramConfig.photo_min_lat, InstagramConfig.photo_min_lng,
	               InstagramConfig.photo_max_lat, InstagramConfig.photo_max_lng]
	r = Region(coordinates)
	now = int(tool.getCurrentStampUTC())
	print now
	buildCorpus(r, [now - 24 *3600, now])