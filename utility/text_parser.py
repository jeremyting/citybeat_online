import operator

from stopwords import Stopwords
import tool


class TextParser:
    def __init__(self, stopword_removal):
        self._word_dict = {}
        self._document_number = 0  # number of documents accumulated
        self._stopword_removal = stopword_removal

    def getTopWords(self, k, percentage=True):
        # if not percentage, it returns the number of photos containing that word.
        if len(self._word_dict) == 0:
            return []
        new_top_words = []
        top_words = sorted(self._word_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
        for i in xrange(0, len(top_words)):
            if percentage:
                value = 1.0 * top_words[i][1] / self._document_number
            else:
                value = top_words[i][1]
            tmp_tuple = (top_words[i][0], value)
            new_top_words.append(tmp_tuple)
        if k == -1:
            return new_top_words
        return new_top_words[0:min(k, len(new_top_words))]

    def insertText(self, cap):
        if cap is None or len(cap) == 0:
            return
        self._document_number = self._document_number + 1
        tmp_dict = self._preprocessText(cap)
        for word in tmp_dict.keys():
            self._word_dict[word] = self._word_dict.get(word, 0) + 1

    def _preprocessText(self, cap):

        new_cap = tool.textPreprocessor(cap)

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
    cp = TextParser(True)
    cap1 = 'gfd #@ @xia@2b #xcv@xcb hahasb@bbb gfd #@ @xia@2b #xcv@xcb hahasb@bbb gfd #@ @xia@2b #xcv@xcb hahasb@bbb'
    cap2 = 'YousbLoveMesb'
    print cp._preprocessText(cap2)