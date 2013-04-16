from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def tokenizer(text):
	return text.split(' ')

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
		
if __name__ == '__main__':
	text1 = 'gfd #@ @xia@2b #xcv@xcb hahasb@bbb gfd #@ @xia@2b #xcv@xcb hahasb@bbb gfd #@ @xia@2b #xcv@xcb hahasb@bbb'
	text2 = 'YousbLoveMesb'
	text3 = 'YousbLoveMesb gdf'
	a = textProprocessor
	print a(text1)
	
	vectorizer = TfidfVectorizer( max_df=0.99, min_df=0, strip_accents='ascii', smooth_idf=True,
																sublinear_tf=True, norm='l2', 
																analyzer='word', ngram_range=(1,1), stop_words = 'english')
	
	documents = [text1, text2, text2, text3, text1, text1, text2, text3]
	print vectorizer.fit_transform(documents)
	print vectorizer.get_feature_names()
	tf_vec = vectorizer.transform([text1]).mean(axis=0)
	nonzeros = np.nonzero(tf_vec)[1]
	res_list = nonzeros.ravel().tolist()[0] 
	print tf_vec