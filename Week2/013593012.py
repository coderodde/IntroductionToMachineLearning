import sys, ast
import loadmovielens as reader
import numpy as np
import math

"""
============================================
DO NOT FORGET TO INCLUDE YOUR STUDENT ID
============================================
"""
student_ID = '013593012'


"load the data into python"
ratings, movie_dictionary, user_ids, item_ids, movie_names = reader.read_movie_lens_data()

def my_info():
    """
    :return: DO NOT FORGET to include your student ID as a string, this function is used to evaluate your code and results
    """
    return student_ID


def Jaccard_Coefficient(movie_id_1, movie_id_2):
    """
    :param movie_id_1: (integer) id regarding the first movie
    :param movie_id2: (integer) id regarding the second movie
    :return: (float) Jaccard_Coefficient regarding these movies based on the given movie IDs
            ROUND OFF TO THREE DECIMAL DIGITS
    """
    if movie_id_1 == movie_id_2:
        return 1.0

    user_ids_a = []
    user_ids_b = []  # rating = [user_id, movie_id]

    for r in ratings:
        if r[1] == movie_id_1:
            user_ids_a.append(r[0])

        if r[1] == movie_id_2:
            user_ids_b.append(r[0])

    s = set(user_ids_a).intersection(set(user_ids_b))
    return round(1.0 * len(s) / (len(user_ids_a) + len(user_ids_b) - len(s)), 3)


def Correlation_Coefficient(movie_id_1, movie_id_2):
    """
    :param movie_id_1: (integer) id regarding the first movie
    :param movie_id2: (integer) id regarding the second movie
    :return: (float) Correlation_Coefficient regarding these movies based on the given movie IDs.
            ROUND OFF TO THREE DECIMAL DIGITS
    """
    if movie_id_1 == movie_id_2:
        return 1.0

    ratings_a = []
    ratings_b = []

    filter_a = set()
    filter_b = set()

    for r in ratings:
        if r[1] == movie_id_1:
            ratings_a.append(r)
            filter_a.add(r[0])

        if r[1] == movie_id_2:
            ratings_b.append(r)
            filter_b.add(r[0])

    common_filter = filter_a.intersection(filter_b)

    pruned_ratings_a = []
    pruned_ratings_b = []

    for r in ratings_a:
        if r[0] in common_filter:
            pruned_ratings_a.append(r)

    for r in ratings_b:
        if r[0] in common_filter:
            pruned_ratings_b.append(r)

    # Now sort the pruned rating lists by user ID's
    pruned_ratings_a.sort(key=lambda x: x[0])
    pruned_ratings_b.sort(key=lambda x: x[0])

    def compute_correlation(ratings_a, ratings_b):
        if len(ratings_a) == 0 or len(ratings_b) == 0:
            return 0.0

        scores_a = [x[2] for x in ratings_a]
        scores_b = [x[2] for x in ratings_b]

        mean_a = np.mean(scores_a)
        mean_b = np.mean(scores_b)

        upper_sum = 0.0
        lower_sum1 = 0.0
        lower_sum2 = 0.0

        for i in range(0, len(scores_a)):
            upper_sum += (scores_a[i] - mean_a) * (scores_b[i] - mean_b)
            lower_sum1 += (scores_a[i] - mean_a) ** 2
            lower_sum2 += (scores_b[i] - mean_b) ** 2

        return upper_sum / math.sqrt(lower_sum1 * lower_sum2)

    return round(compute_correlation(pruned_ratings_a, pruned_ratings_b), 3)


def main():
    """
    DO NOT TOUCH THIS FUNCTION. IT IS USED FOR COMPUTER EVALUATION OF YOUR CODE
    """
    test_cases = ast.literal_eval(sys.argv[1])
    results = str(my_info()) + '\t\t'
    for test_case in test_cases:
        mode = test_case[0]
        id_1 = int(test_case[1])
        id_2 = int(test_case[2])
        if mode == 'jc':
            results += str(Jaccard_Coefficient(id_1, id_2)) + '\t\t'
        elif mode == 'cc':
            results += str(Correlation_Coefficient(id_1, id_2)) + '\t\t'
        else:
            exit('bad command')
    print results + '\n'

if __name__ == '__main__':
    main()
