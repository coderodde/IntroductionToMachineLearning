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

toy_story_id  = reader.give_me_movie_id('Toy Story', movie_dictionary)[0][0]
golden_eye_id = reader.give_me_movie_id('GoldenEye', movie_dictionary)[0][0]

print toy_story_id
print golden_eye_id
print jaccard_coefficient(toy_story_id, golden_eye_id)