import loadmovielens as reader

ratings, movie_dictionary, user_ids, item_ids, movie_names = reader.read_movie_lens_data()

#print(ratings[0])

def jaccard_coefficient(movie_id_a, movie_id_b):
    if movie_id_a == movie_id_b:
        return 1.0

    user_ids_a = []
    user_ids_b = [] #rating = [user_id, movie_id]

    for r in ratings:
        if r[1] == movie_id_a:
            user_ids_a.append(r[0])

        if r[1] == movie_id_b:
            user_ids_b.append(r[0])

    s = set(user_ids_a).intersection(set(user_ids_b))
    return 1.0 * len(s) / (len(user_ids_a) + len(user_ids_b) - len(s))

def coefficient_compare(a, b):
    return a[1] > b[1]

# Given the movie ID and an integer k, find out the list with atmost
# k movies IDs that are closest to the target movie ID.
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

    print "Map size: ", len(map_from_movie_to_user_id_list)

    ret = sorted(ret, key=lambda x: -x[1])

    while len(ret) > k:
        ret.pop()

    for t in ret:
        print t[0], " ", t[1]

print "Closest 5"
print find_k_closest(1, 5)

toy_story_id  = reader.give_me_movie_id('Toy Story', movie_dictionary)[0][0]
golden_eye_id = reader.give_me_movie_id('GoldenEye', movie_dictionary)[0][0]

print jaccard_coefficient(toy_story_id, golden_eye_id)

red_id  = reader.give_me_movie_id('Three Colors: Red', movie_dictionary)[0][0]
blue_id = reader.give_me_movie_id('Three Colors: Blue', movie_dictionary)[0][0]

print jaccard_coefficient(red_id, blue_id)