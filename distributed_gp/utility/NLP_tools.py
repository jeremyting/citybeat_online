from stopwords import Stopwords

import operator


class ElementParser:
	
	@staticmethod
	def parseText(cap):
		
		def removeAt(cap):
			# remove @eddie
			new_cap = ''
			for word in cap.split(' '):
				word = word.strip()
				if word == '':
					continue
				if word.startswith('@'):
					continue
				new_cap += word + ' '
			return new_cap.strip()
			
		cap = removeAt(cap)
		
		# change the word YouLoveMe into you love me seperately
		new_cap = ''
		pre_is_cap = False
		for c in cap:
			if c.isupper():
				if not pre_is_cap:
					new_cap += ' '
				new_cap += c.lower()
				pre_is_cap = True
				continue

			if c.islower():
				new_cap += c
			else:
				new_cap += ' '
			pre_is_cap = False
			 
		words = new_cap.split()
		stopword_list = Stopwords.stopwords()
		tmp_dict = {} 
		
		for word in words:
			word = word.strip()
			if self._stopword_removal and word in stopword_list:
				continue
			if len(word) < 3:
				continue
			if word in tmp_dict.keys():
				tmp_dict[word] = tmp_dict[word] + 1
			else:
				tmp_dict[word] = 1
		return tmp_dict
		
if __name__ == '__main__':
	cp = CaptionParser(True)
	cap1 = 'gfd #@ @xia@2b #xcv@xcb hahasb@bbb gfd #@ @xia@2b #xcv@xcb hahasb@bbb gfd #@ @xia@2b #xcv@xcb hahasb@bbb'
	cap2 = 'YousbLoveMesb'
	print CaptionParser.parse(cap2)