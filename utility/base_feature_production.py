from event_interface import EventInterface
from base_feature import BaseFeature
from corpus import buildAllCorpus


class BaseFeatureProduction(BaseFeature):
    # the only difference betweetn this class and BaseFeature is that this 
    # class does not provide label

    def __init__(self, event, corpus=None, representor=None):
        super(BaseFeatureProduction, self).__init__(event, corpus, representor)

    def extractFeatures(self, entropy_para=3, k_topwords=3):
        # it outputs the feature vector
        self.preprocess()
        avg_cap_len = self.getAvgTextLen()
        dis_feautures = self.getElementDisFeatures()
        std_element_dis = dis_feautures[0]
        avg_element_dis = dis_feautures[1]
        avg_element_dis_cap = self.getElementTextDisFeatures()[1]
        cap_per = self.getTextPercentage()
        std = self.getPredictedStd()
        top_word_pop = self.getTopWordPopularity(k_topwords)
        zscore = self.getZscore()
        entropy = self.getEntropy(entropy_para)

        event_id = str(self._event['_id'])

        tfidf_top3 = self.getTopWordByTFIDF(3)
        res = self.countHashtagFromElementContainingTopKeyword(3)
        hashtage_cnt3 = res[0]
        number_elements_associated_with_keywords3 = res[1]

        # for test only
        #historic_features = [0]*3  
        historic_features = self.getHistoricFeatures(entropy_para)
        diff_avg_element_dis = avg_element_dis - historic_features[0]
        diff_top_word_pop = historic_features[1]
        diff_entropy = historic_features[2]

        location_name_similarity = self.getTopElementsLocationSimilarity()

        return [avg_cap_len,
                std_element_dis, avg_element_dis,
                avg_element_dis_cap,
                cap_per,
                std, top_word_pop, zscore, entropy, #ratio,
                diff_avg_element_dis, diff_top_word_pop, diff_entropy,
                tfidf_top3[0], tfidf_top3[1], tfidf_top3[2],
                hashtage_cnt3[0], hashtage_cnt3[1], hashtage_cnt3[2],
                number_elements_associated_with_keywords3[0], number_elements_associated_with_keywords3[1],
                number_elements_associated_with_keywords3[2],
                location_name_similarity,
                event_id]


def testWithPhoto():
    corpus_all = buildAllCorpus(element_type='photos', debug=True)
    for key, corpus in corpus_all.items():
        break

    ei = EventInterface()
    ei.setDB('citybeat')
    ei.setCollection('candidate_event_25by25_merged')
    event = ei.getDocument()
    event = BaseFeatureProduction(event, corpus=corpus)
    print event.extractFeatures()


if __name__ == '__main__':
    testWithPhoto()
    # print '*************************'