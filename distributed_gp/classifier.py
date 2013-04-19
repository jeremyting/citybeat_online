"""
Given training data, training the model, and then return a classifier to classify
future candidate event.

"""
from sklearn import preprocessing
from sklearn import linear_model, decomposition, datasets
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from numpy import genfromtxt

import random
import numpy as np



def getPositiveSamples( data ):
    training = [data[0,:]]
    testing = [data[1,:]]


    for row in data[2:180, :]:
        r = random.random()
        if r <0.83:
            # positive
            training = np.concatenate( (training,[row])) 
        else:
            # neg
            testing = np.concatenate( (testing, [row]) ) 
    n, m = data.shape
    
    for row in data[181:n, :]:
        r = random.random()
        if r < 0.11 :
            training = np.concatenate((training, [row]))
        elif r>=0.11 and r<=0.29:
            testing = np.concatenate((testing, [row] ))
    
    return training, testing


class Classifier:
    def __init__(self):
        my_data = genfromtxt('181.csv', delimiter=',')
        
        
        #format of the training file should be, each row is a example and the last column is the label. column N-2 is the id of the event
        #let's label them as 0, 1
        m, n = my_data.shape
        #my_data[:,0:n-2] = preprocessing.scale(my_data[:,0:n-2])
        for i in range(m):
            if my_data[i,n-1]<0.0:
                my_data[i,n-1] = 0
            else:
                my_data[i,n-1] = 1
        

        training, testing = getPositiveSamples( my_data )

        training_matrix = training[:, 0:n-2]
        training_label = training[:, n-1]
        testing_matrix = testing[:, 0:n-2]
        testing_label = testing[:, n-1]
        

        self.scaler = preprocessing.StandardScaler().fit(training_matrix)
        print 'before transform'
        print training_matrix 
        self.scaler_test = preprocessing.StandardScaler().fit(testing_matrix)
        training_matrix = self.scaler.transform(training_matrix)
        print 'after transform'
        print training_matrix
        testing_matrix = self.scaler.transform(testing_matrix)
        #self.clf= SVC(kernel="linear", C=0.15)

        self.clf =  linear_model.LogisticRegression()
        #self.clf  = KNeighborsClassifier(5)
        #knn.fit(training_matrix, training_label)
        #Z = knn.predict(testing_matrix)
        #Z = logistic.predict(testing_matrix)
        
        
        
        self.clf.fit(training_matrix, training_label)
        Z = self.clf.predict(testing_matrix)
        cm = confusion_matrix(Z, testing_label)
        report = classification_report(testing_label, Z) 
        print report
        #Z = logistic.predict(training_matrix)
        #cm = confusion_matrix(Z, training_label)

        print 'positive # ', sum(training_label)
        print 'training matrix shape ', training_matrix.shape
        print 'testing matrix shape ' , testing_matrix.shape
        print cm

    def classify(self,feature_vector):
        #given a feature vector, return it's label
        fv = self.scaler.transform(np.asarray(feature_vector[:-1]))
        Z = self.clf.predict( fv) 
        Z_prob = self.clf.predict_proba(fv)
        #print 'classify as ',Z
        #print feature_vector[-1],Z[0]
        if Z_prob[1]>0.9:
            print 'prob = ',Z_prob

def test():
    clf = Classifier()
    clf.classify([67.684211,0.048597,0.340716,7.645089,0.95,2.300865,0.087719,4.043987,2.969329,-0.028381,20.056143,0.275494,0.300945,0.275448,0.25635,0.5,0,0,2,2,1,0.1, 'kjdsfsdkjf'])


def main():
    test()


if __name__=='__main__':
    main()
