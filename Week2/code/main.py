import loadmovielens as reader
import numpy as np
import math

ratings, movie_dictionary, user_ids, item_ids, movie_names = reader.read_movie_lens_data()


def jaccard_coefficient(movie_id_a, movie_id_b):
    if movie_id_a == movie_id_b:
        return 1.0

    user_ids_a = []
    user_ids_b = []  # rating = [user_id, movie_id]

    for r in ratings:
        if r[1] == movie_id_a:
            user_ids_a.append(r[0])

        if r[1] == movie_id_b:
            user_ids_b.append(r[0])

    s = set(user_ids_a).intersection(set(user_ids_b))
    return 1.0 * len(s) / (len(user_ids_a) + len(user_ids_b) - len(s))


def coefficient_compare(a, b):
    return a[1] > b[1]


# Given the movie ID 'target_movie_id' and an integer 'k',
# find out the list with at most 'k' entries containing tuples
# (movie_id, Jaccard) that are closest by Jaccard coefficient to
# the movie with the ID 'target_movie_id'.
def find_k_closest(target_movie_id, k):
    map_from_movie_to_user_id_list = dict()

    # Map each movie id to the list of users who have seen that movie.
    for r in ratings:
        movie_id = r[1]
        user_id = r[0]
        if map_from_movie_to_user_id_list.has_key(movie_id):
            map_from_movie_to_user_id_list[movie_id].append(user_id)
        else:
            map_from_movie_to_user_id_list[movie_id] = [user_id]

    # Build the array of tuples, where each tuple is of the format
    # (movie_id, jaccard coefficient to the target movie).
    ret = []

    def fast_jaccard_coefficient(user_ids_a, user_ids_b):
        s = set(user_ids_a).intersection(set(user_ids_b))
        return 1.0 * len(s) / (len(user_ids_a) + len(user_ids_b) - len(s))

    for movie_id in map_from_movie_to_user_id_list:
        ret.append((movie_id,
                    fast_jaccard_coefficient(map_from_movie_to_user_id_list[movie_id],
                                             map_from_movie_to_user_id_list[target_movie_id])))

    ret = sorted(ret, key=lambda x: -x[1])

    while len(ret) > k + 1:
        ret.pop()

    return ret[1:k + 1]


print "--- Jaccard coefficient between 'Toy Story' and 'GoldenEye' ---"
toy_story_id = reader.give_me_movie_id('Toy Story', movie_dictionary)[0][0]
golden_eye_id = reader.give_me_movie_id('GoldenEye', movie_dictionary)[0][0]

print jaccard_coefficient(toy_story_id, golden_eye_id)

print "--- Jaccard coefficient between 'Three Colors: Red' and 'Three Colors: Blue' ---"
red_id = reader.give_me_movie_id('Three Colors: Red', movie_dictionary)[0][0]
blue_id = reader.give_me_movie_id('Three Colors: Blue', movie_dictionary)[0][0]

print jaccard_coefficient(red_id, blue_id)

print "--- Closest 5 movies to 'Taxi Driver'---"
taxi_driver_id = reader.give_me_movie_id('Taxi Driver', movie_dictionary)[0][0]
taxi_passengers = find_k_closest(taxi_driver_id, 5)

for t in taxi_passengers:
    print movie_names[t[0]], ", coefficient: ", t[1]

print "--- Closest 5 movies to 'Star Wars (1977) ---"
star_wars_id = reader.give_me_movie_id('Star Wars', movie_dictionary)[0][0]
star_warriors = find_k_closest(star_wars_id, 5)

for s in star_warriors:
    print movie_names[s[0]], ", coefficient: ", s[1]


def compute_correlation(ratings_a, ratings_b):
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


def correlation_coefficient(movie_id_a, movie_id_b):
    if movie_id_a == movie_id_b:
        return 1.0

    ratings_a = []
    ratings_b = []

    filter_a = set()
    filter_b = set()

    for r in ratings:
        if r[1] == movie_id_a:
            ratings_a.append(r)
            filter_a.add(r[0])

        if r[1] == movie_id_b:
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

    return compute_correlation(pruned_ratings_a, pruned_ratings_b)


print "--- Correlation coefficient between 'Toy Story' and 'GoldenEye' ---"
print correlation_coefficient(toy_story_id, golden_eye_id)

print "--- Correlation coefficient between 'Three Colors: Red' and 'Three Color: Blue' ---"
print correlation_coefficient(red_id, blue_id)
