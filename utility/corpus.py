from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from photo_interface import PhotoInterface
from tweet_interface import TweetInterface
from region import Region
from config import InstagramConfig
from config import TwitterConfig
import tool
import logging

class Corpus(object):
    def buildCorpus(self, region, time_interval, element_type='photos', paras={}):
        # time_interval should be [start, end]
        text = []
        if element_type == 'photos':
            ei = PhotoInterface()
            cur = ei.rangeQuery(region, time_interval, 'caption.text')
        else:
            ei = TweetInterface()
            cur = ei.rangeQuery(region, time_interval, 'text')
        for t in cur:
            try:
                if element_type == 'photos':
                    text.append(t['caption']['text'])
                else:
                    text.append(t['text'])
            except:
                pass

        # it is not proper here to set up stopwords
        self._vectorizer = TfidfVectorizer(max_df=paras.get('max_df', 0.2),
                                           min_df=paras.get('min_df', 0.0),
                                           strip_accents=paras.get('strip_accents', 'ascii'),
                                           preprocessor=paras.get('preprocessor', tool.textPreprocessor),
                                           smooth_idf=paras.get('smooth_idf', True),
                                           sublinear_tf=paras.get('sublinear_tf', True),
                                           norm=paras.get('norm', 'l2'),
                                           analyzer=paras.get('analyzer', 'word'),
                                           ngram_range=paras.get('ngram_range', (1, 1)),
                                           stop_words=paras.get('stop_words', 'english')
        )

        # If the program do not break here, we may ignore the bug
        try:
            self._vectorizer.fit_transform(text)
        except Exception as error :
            logging.warn(error)

    def getVectorizer(self):
        return self._vectorizer

    def chooseTopWordWithHighestTDIDF(self, text, k=10):
        voc = self._vectorizer.get_feature_names()
        tf_vec = self._vectorizer.transform([text]).mean(axis=0)
        nonzeros = np.nonzero(tf_vec)[1]
        res_list = nonzeros.ravel().tolist()[0]
        values = []
        words = []
        for n in res_list:
            words.append(voc[n])
            values.append(tf_vec[0, n])
        while len(values) < k:
            values.append(0)
            #return res_list, words, values
        return values


def buildAllCorpus(element_type='photos', time_interval_length=14, debug=False, paras={}):
    # return a dict = {region : its local corpus}
    assert element_type in ['photos', 'tweets']

    all_corpus = {}
    if element_type == 'photos':
        config = InstagramConfig
    else:
        config = TwitterConfig

    coordinates = [config.min_lat, config.min_lng,
                   config.max_lat, config.max_lng]

    nyc = Region(coordinates)
    region_list = nyc.divideRegions(25, 25)
    region_list = nyc.filterRegions(region_list, test=True, n=25, m=25, element_type=element_type)

    # 14 days ago
    now = int(tool.getCurrentStampUTC())

    num = 0
    for region in region_list:
        if debug and num > 0:
            # speed up the debugging
            pass
        else:
            cor = Corpus()
            cor.buildCorpus(region, [now - time_interval_length * 3600 * 24, now], element_type, paras)
        all_corpus[region.getKey()] = cor
        num += 1
        print 'build corpus %d' % (num)
    return all_corpus


if __name__ == '__main__':
    buildAllCorpus(element_type='photos')