import mnist_load_show as mnist

X, y = mnist.read_mnist_training_data()

import numpy as np
import mnist_load_show as mnist
"""
============================================
DO NOT FORGET TO INCLUDE YOUR STUDENT ID
============================================
"""
student_ID = '013593012'

# Read data
X, y = mnist.read_mnist_training_data()

# Split into training and testing sets
XTrain = X[0:30000]
XTest  = X[30000:60000]

yTrain = y[0:30000]
yTest  = y[30000:60000]



def my_info():
    return student_ID


def one_vs_all():
    #### LEARN ####
    # w_classes is an array of length 10 holding the w-vector for each class.
    # The ith vector corresponds to the class 'i'.
    w_classes = [np.array([0 for i in range(len(XTrain[0]))]) for cls in range(10)]

    for i in range(len(XTrain)):
        X = XTrain[i]
        y = yTrain[i]
        y_classified = np.sign(np.dot(w_classes[y], X))

        if y_classified != 1:
            w_classes[y] += y * X

    #### CLASSIFY ####
    # Create confusion matrix:
    confusion_matrix = [[0 for i in range(10)] for j in range(10)]

    # Iterate over the test data.
    for i in range(len(XTest)):
        X = XTest[i]
        y = yTest[i]

        best_score = 0
        best_class = -1

        # Try against each class:
        for cls in range(10):
            score = np.dot(w_classes[cls], X)
            if best_score < score:
                best_score = score
                best_class = cls

        # Update confusion matrix:
        confusion_matrix[y][best_class] += 1
    # Done iterating over the test data.
    one_vs_all_conf_matrix = []
    return one_vs_all_conf_matrix

one_vs_all()


def all_vs_all():
    all_vs_all_conf_matrix = ''
    return all_vs_all_conf_matrix




def main():
    """
    DO NOT TOUCH THIS FUNCTION. IT IS USED FOR COMPUTER EVALUATION OF YOUR CODE
    """
    results = my_info() + '\t\t'
    results += np.array_str(np.diagonal(one_vs_all())) + '\t\t'
    results += np.array_str(np.diagonal(all_vs_all()))
    print results + '\t\t'

# Uncomment me!
#if __name__ == '__main__':
    #main()