import numpy as np
import mnist_load_show as mnist

'''
use pdis in order to find the the distance
'''
from scipy.spatial.distance import cdist

"""
============================================
DO NOT FORGET TO INCLUDE YOUR STUDENT ID
============================================
"""
student_ID = '013593012'

TOTAL_IMAGES = 5000
### LOAD ########THE DATA #########################
X, y = mnist.read_mnist_training_data(TOTAL_IMAGES)
###################################################

#print "len(X): ", len(X), ", len(y): ", len(y)
indices = np.random.choice(5000, 100, replace=False)
mnist.visualize(X[indices])
print y[indices]

def split(X):
    XTrain = []
    XTest  = []

    yTrain = []
    yTest  = []

    length = len(X)
    half   = length / 2

    for i in range(0, half):
        XTrain.append(X[i])
        yTrain.append(y[i])

    for i in range(half, length):
        XTest.append(X[i])
        yTest.append(y[i])

    return XTrain, XTest, yTrain, yTest

def my_info():
    """
    :return: DO NOT FORGET to include your student ID as a string, this function is used to evaluate your code and results
    """
    return student_ID


def KNN():
    """
    Implement the classifier using KNN and return the confusion matrix
    :return: the confusion matrix regarding the result obtained using knn method
    """
    knn_conf_matrix = ''
    return knn_conf_matrix


def simple_EC_classifier():
    """
    Implement the classifier based on the Euclidean distance
    :return: the confusing matrix obtained regarding the result obtained using simple Euclidean distance method
    """
    simple_EC_conf_martix = ''
    return simple_EC_conf_martix




def main():
    """
    DO NOT TOUCH THIS FUNCTION. IT IS USED FOR COMPUTER EVALUATION OF YOUR CODE
    """
    results = my_info() + '\t\t'
    results += np.array_str(np.diagonal(simple_EC_classifier())) + '\t\t'
    results += np.array_str(np.diagonal(KNN()))
    print results + '\n'

### REMEMBER TO UNCOMMENT ME ###
#if __name__ == '__main__':
#    main()
