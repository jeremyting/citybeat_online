from corpus import buildAllCorpus
from event_interface import EventInterface
from tweet_interface import TweetInterface
from base_feature import BaseFeature

class TwitterFeature(BaseFeature):
    # the only difference betweetn this class and BaseFeature is that this 
    # class does not provide label
    
    def __init__(self, event, corpus=None, representor=None):
        super(TwitterFeature, self).__init__(event, corpus, representor)

    @staticmethod
    def GenerateArffFileHeader():
        print '@relation CityBeatEvents'
        print '@attribute AvgTextLen real'
#       print '@attribute stat_MinElementDis real'
#       print '@attribute stat_MaxElementDis real'
        print '@attribute stat_StdElementDis real'
        print '@attribute AvgElementDis real'
#       print '@attribute stat_MedianElementDis real'
#       print '@attribute stat_MinElementDisbyCap real'
#       print '@attribute stat_MaxElementDisbyCap real'
#       print '@attribute stat_StdElementDisbyCap real'
        print '@attribute AvgElementDisbyCap real'
#       print '@attribute stat_MedianElementDisbyCap real'
        print '@attribute TextPercentage real'
        print '@attribute PredictedStd real'
        print '@attribute TopWordPopularity real'
        print '@attribute Zscore real'
        print '@attribute Entropy real'
        print '@attribute diff_AvgElementDis real'
        print '@attribute diff_TopWordPopularity real'
        print '@attribute diff_Entropy real'

        print '@attribute tfidf1 real'  
        print '@attribute tfidf2 real'  
        print '@attribute tfidf3 real'
        
        print '@attribute NumberOfhashtags1 real'   
        print '@attribute NumberOfhashtags2 real'   
        print '@attribute NumberOfhashtags3 real'   
        
        print '@attribute NumberOfPhotsContaingTopWord1 real'
        print '@attribute NumberOfPhotsContaingTopWord2 real'
        print '@attribute NumberOfPhotsContaingTopWord3 real'
                                
        print '@attribute ID string'
        print '@attribute label {1,-1}'

        print '@data'

    def extractFeatures(self, entropy_para=3, k_topwords=3):
        # twitter feature has no location similarity
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
        historic_features = [0]*3  
      #  historic_features = self.getHistoricFeatures(entropy_para)
        diff_avg_element_dis = avg_element_dis - historic_features[0]
        diff_top_word_pop = historic_features[1]
        diff_entropy = historic_features[2]
        
        return [avg_cap_len,
				std_element_dis, avg_element_dis, 
                avg_element_dis_cap,
                cap_per,
                std, top_word_pop, zscore, entropy, #ratio,
                diff_avg_element_dis, diff_top_word_pop, diff_entropy,
                tfidf_top3[0], tfidf_top3[1], tfidf_top3[2], 
                hashtage_cnt3[0], hashtage_cnt3[1], hashtage_cnt3[2],
                number_elements_associated_with_keywords3[0], number_elements_associated_with_keywords3[1], number_elements_associated_with_keywords3[2],
                event_id]

def testWithTweet():
    corpus_all = buildAllCorpus(element_type='tweets', debug=True)
    for key, corpus in corpus_all.items():
        break

    ei = EventInterface()
    ei.setDB('citybeat_experiment')
    ei.setCollection('twitter_candidate_events')
    cur = ei.getAllDocuments()
    for event in cur:
        event = TwitterFeature(event, corpus=corpus)
        event.printFeatures()

if __name__=='__main__':
    # testWithPhoto()
    # print '*************************'
    testWithTweet()