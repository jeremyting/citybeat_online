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

    print np.concatenate( (training, testing), axis =0)

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
        print 'In classifier'
        my_data = genfromtxt('181.csv', delimiter=',')
        m, n = my_data.shape
        
        my_data[:,0:n-2] = preprocessing.scale(my_data[:,0:n-2])
        
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
    

        svc =     SVC(kernel="linear", C=0.15)
        svc.fit(training_matrix, training_label)
        Z = svc.predict(testing_matrix)

        #logistic = linear_model.LogisticRegression()
        #logistic.fit(training_matrix, training_label)
        
        #knn = KNeighborsClassifier(5)
        #knn.fit(training_matrix, training_label)
        #Z = knn.predict(testing_matrix)

        #Z = logistic.predict(testing_matrix)
        cm = confusion_matrix(Z, testing_label)

        report = classification_report(testing_label, Z) 
        print report
        #Z = logistic.predict(training_matrix)
        #cm = confusion_matrix(Z, training_label)

        print 'positive # ', sum(training_label)


        print 'training matrix shape ', training_matrix.shape
        print 'testing matrix shape ' , testing_matrix.shape

        print cm


        

def test():
    Classifier()



def main():
    test()


if __name__=='__main__':
    main()
