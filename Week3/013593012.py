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


def split(X, y):
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

def compute_prototype(XTrain, yTrain, digit):
    prototype = np.array([0 for x in range(0, len(XTrain[0]))])
    count = 0
    length = len(XTrain)

    for index in range(0, length):
        if yTrain[index] == digit:
            count += 1
            prototype += XTrain[index]

    return prototype / count

def create_prototypes(XTrain, yTrain):
    prototypes = []

    for digit in range(0, 10):
        prototypes.append(compute_prototype(XTrain, yTrain, digit))

    return np.array(prototypes)

XTrain, XTest, yTrain, yTest = split(X, y)
prototypes = create_prototypes(XTrain, yTrain)

def error_rate(conf_matrix):
    total = 0
    matches = 0
    n = len(conf_matrix)

    for y in range(0, n):
        for x in range(0, n):
            total += conf_matrix[y][x]

    for i in range(0, n):
        matches += conf_matrix[i][i]

    accuracy = 1.0 * matches / total
    return 1 - accuracy

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
    predicted_labels = []
    distance_matrix = cdist(XTest, XTrain, 'euclidean')

    def find_best_label(dist_vector):
        best_index = 0
        best_distance = dist_vector[0]

        for index in range(1, len(dist_vector)):
            tentative_dist = dist_vector[index]
            if best_distance > tentative_dist:
                best_distance = tentative_dist
                best_index = index

        return yTrain[best_index]

    for i in range(0, len(distance_matrix)):
        predicted_labels.append(find_best_label(distance_matrix[i]))

    confusion_matrix = [[0 for i in range(0, 10)] for j in range(0, 10)]

    for i in range(0, len(predicted_labels)):
        y = yTest[i]
        x = predicted_labels[i]
        confusion_matrix[y][x] += 1

    #for y in range(0, len(confusion_matrix)):
    #    print confusion_matrix[y]

    #print error_rate(confusion_matrix)
    return confusion_matrix


def simple_EC_classifier():
    """
    Implement the classifier based on the Euclidean distance
    :return: the confusing matrix obtained regarding the result obtained using simple Euclidean distance method
    """
    predicted_labels = []
    distance_matrix = cdist(XTest, prototypes, 'euclidean')

    def find_best_label(dist_vector):
        best_digit = 0
        best_dist = dist_vector[0]

        for digit in range(1, len(dist_vector)):
            tentative_dist = dist_vector[digit]
            if best_dist > tentative_dist:
                best_dist = tentative_dist
                best_digit = digit

        return best_digit

    for i in range(0, len(distance_matrix)):
        predicted_labels.append(find_best_label(distance_matrix[i]))

    confusion_matrix = [[0 for i in range(0, 10)] for j in range(0, 10)]

    for i in range(0, len(predicted_labels)):
        y = yTest[i]
        x = predicted_labels[i]
        confusion_matrix[y][x] += 1

    #for y in range(0, len(confusion_matrix)):
    #    print confusion_matrix[y]

    #print error_rate(confusion_matrix)
    return confusion_matrix

#print "*** Prototype classifier ***"
#simple_EC_classifier()
#print "*** KNN ***"
#KNN()

def main():
    """
    DO NOT TOUCH THIS FUNCTION. IT IS USED FOR COMPUTER EVALUATION OF YOUR CODE
    """
    results = my_info() + '\t\t'
    results += np.array_str(np.diagonal(simple_EC_classifier())) + '\t\t'
    results += np.array_str(np.diagonal(KNN()))
    print results + '\n'

if __name__ == '__main__':
    main()
