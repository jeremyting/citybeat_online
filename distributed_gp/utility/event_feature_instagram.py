from base_feature import BaseFeature

class BaseFeature(BaseFeature):
    
    def __init__(self, event, corpus=None, representor=None):
        super(BaseFeature, self).__init__(event)
        # note that, if you want to use any feature related with tfidf, corpus must be set
        # the the definition of Corpus class in corpus.py
        if corpus is not None:
            self._corpus = corpus
        if representor is not None:
            self._representor = representor
    
    def extractFeatures(self, entropy_para=3, k_topwords=3):
        # it outputs the feature vector
        self.preprocess()
        avg_cap_len = self.getAvgCaptionLen()
        dis_feautures = self.getPhotoDisFeatures()
        min_photo_dis = dis_feautures[0]
        max_photo_dis = dis_feautures[1]
        std_photo_dis = dis_feautures[2]
        avg_photo_dis = dis_feautures[3]
        median_photo_dis = dis_feautures[4]
        cap_dis_features = self.getPhotoCaptionDisFeatures()
        min_photo_dis_cap = cap_dis_features[0]
        max_photo_dis_cap = cap_dis_features[1]
        std_photo_dis_cap = cap_dis_features[2]
        mean_photo_dis_cap = cap_dis_features[3]
        median_photo_dis_cap = cap_dis_features[4]
        cap_per = self.getCaptionPercentage()
        std = self.getPredictedStd()
        top_word_pop = self.getTopWordPopularity(k_topwords)
        zscore = self.getZscore()
        entropy = self.getEntropy(entropy_para)
        event_id = str(self._event['_id'])
        tfidf_top3 = self.getTopWordByTFIDF(3)
        res = self.countHashtagsFromPhotosContainingTopKeywords(3)
        hashtage_cnt3 = res[0]
        number_photos_associated_with_keywords3 = res[1]
        historic_features = self.getHistoricFeatures(entropy_para)
        diff_avg_photo_dis = avg_photo_dis - historic_features[0]
        diff_top_word_pop = historic_features[1]
        diff_entropy = historic_features[2]
        
        location_name_similarity = self.getTopPhotosLocationSimilarity()
        
        return [avg_cap_len,
                        std_photo_dis, avg_photo_dis, 
                mean_photo_dis_cap,
                cap_per,
                std, top_word_pop, zscore, entropy, #ratio,
                diff_avg_photo_dis, diff_top_word_pop, diff_entropy,
                tfidf_top3[0], tfidf_top3[1], tfidf_top3[2], 
                hashtage_cnt3[0], hashtage_cnt3[1], hashtage_cnt3[2],
                number_photos_associated_with_keywords3[0], number_photos_associated_with_keywords3[1], number_photos_associated_with_keywords3[2],
                location_name_similarity, 
                event_id]
    
            
if __name__=='__main__':
    pass