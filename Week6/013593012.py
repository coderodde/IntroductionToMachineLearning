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

def copy(source, target):
    for y in range(len(source)):
        for x in range(len(source[y])):
            target[y][x] = source[y][x]


def one_vs_all():
    #### LEARN ####
    # w_classes is an array of length 10 holding the w-vector for each class.
    # The ith vector corresponds to the class 'i'.
    w_classes = [np.array([0 for i in range(len(XTrain[0]))]) for cls in range(10)]
    pocket_w_classes = [np.array([0 for i in range(len(XTrain[0]))]) for cls in range(10)]
    pocket_score = 0
    pocket_changed = True

    while pocket_changed:
        score = 0
        pocket_changed = False

        for i in range(len(XTrain)):
            X = XTrain[i]
            actual_class = yTrain[i]
            best_class = 0
            best_cost = np.dot(w_classes[0], X)

            for cls in range(1, 10):
                current_cost = np.dot(w_classes[cls], X)

                if best_cost < current_cost:
                    best_cost = current_cost
                    best_class = cls

            if best_class != actual_class:
                w_classes[best_class] -= X
                w_classes[actual_class] += X

                if score > pocket_score:
                    pocket_score = score
                    copy(w_classes, pocket_w_classes)
                    pocket_changed = True

                score = 0
            else:
                score += 1

    #### CLASSIFY ####
    # Create confusion matrix:
    confusion_matrix = [[0 for i in range(10)] for i in range(10)]

    # Iterate over the test data.
    for i in range(len(XTest)):
        X = XTest[i]
        actual_class = yTest[i]

        best_score = 0
        best_class = -1

        # Try against each class:
        for cls in range(10):
            score = np.dot(pocket_w_classes[cls], X)
            if best_score < score:
                best_score = score
                best_class = cls

        # Update confusion matrix:
        confusion_matrix[best_class][actual_class] += 1
    # Done iterating over the test data.
    return confusion_matrix

#matrix = one_vs_all()

#for i in range(len(matrix)):
#    print(matrix[i])

#sum = 0

#for i in range(len(matrix)):
#    sum += matrix[i][i]

#print("Correct", sum)

def all_vs_all():
    all_vs_all_conf_matrix = [[1 for i in range(10)] for j in range(10)]
    return all_vs_all_conf_matrix


def main():
    """
    DO NOT TOUCH THIS FUNCTION. IT IS USED FOR COMPUTER EVALUATION OF YOUR CODE
    """
    conf_matrix1 = one_vs_all()
    conf_matrix2 = all_vs_all()
    results = my_info() + '\t\t'
    results += np.array_str(np.diagonal(conf_matrix1)) + '\t\t'
    results += np.array_str(np.diagonal(conf_matrix2))
    print results + '\t\t'
    sum = 0
    for i in range(10):
        sum += conf_matrix1[i][i]
    print "Sum:", sum




if __name__ == '__main__':
    main()