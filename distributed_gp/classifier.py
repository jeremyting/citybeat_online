"""
Given training data, training the model, and then return a classifier to classify
future candidate event.

"""

from sklearn import linear_model, decomposition, datasets
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
        if r < 0.11:
            training = np.concatenate((training, [row]))
        else:
            testing = np.concatenate((testing, [row] ))
    
    return training, testing


class Classifier:
    def __init__(self):
        print 'In classifier'
        my_data = genfromtxt('181.csv', delimiter=',')
        training, testing = getPositiveSamples( my_data )
        

        m, n = training.shape

        training_matrix = training[:, 0:n-2]
        training_label = training[:, n-1]

        testing_matrix = testing[:, 0:n-2]
        testing_label = testing[:, n-1]
    

        
        logistic = linear_model.LogisticRegression()
        logistic.fit(training_matrix, training_label)


        

def test():
    Classifier()



def main():
    test()


if __name__=='__main__':
    main()
