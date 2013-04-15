from stopwords import Stopwords

import operator

class TextParser(object):
	
	def parse2(self, text):
		print text
	
	@staticmethod
	def parse(text):
		
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
			 
		words = new_text.split()
		stopword_list = Stopwords.stopwords()
		tmp_dict = {} 
		
		for word in words:
			word = word.strip()
			if len(word) < 3:
				continue
			if word in tmp_dict.keys():
				tmp_dict[word] = tmp_dict[word] + 1
			else:
				tmp_dict[word] = 1
		return tmp_dict
		
if __name__ == '__main__':
	tp = TextParser()
	text1 = 'gfd #@ @xia@2b #xcv@xcb hahasb@bbb gfd #@ @xia@2b #xcv@xcb hahasb@bbb gfd #@ @xia@2b #xcv@xcb hahasb@bbb'
	text2 = 'YousbLoveMesb'
	a = tp.parse2
	a(text2)