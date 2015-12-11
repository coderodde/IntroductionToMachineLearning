import mnist_load_show as mnist
import numpy as np

X, y = mnist.read_mnist_training_data()


def kmeans(data_matrix, initial_cluster_means):
    assignment = dict()
    cluster_means = initial_cluster_means.copy()

    while True:
        # Assign the new vector to a cluster
        for i in range(len(data_matrix)):
            best_cluster_id = -1
            best_distance = 1000000000.0

            for k in range(10):
                dist = np.linalg.norm(data_matrix[i] - cluster_means[k])
                dist *= dist # squared Euclidean distance

                if best_distance > dist:
                    best_distance = dist
                    best_cluster_id = k

            assignment[i] = best_cluster_id

        # Update the cluster means
        new_cluster_means = np.zeros([10, len(initial_cluster_means[0])])
        cluster_sizes = [0 for ii in range(10)]

        for i in range(len(data_matrix)):
            cluster_id = assignment[i]
            new_cluster_means[cluster_id] += data_matrix[i]
            cluster_sizes[cluster_id] += 1

        for i in range(10):
            new_cluster_means[i] /= cluster_sizes[i]

        if np.array_equal(new_cluster_means, cluster_means):
            break

        cluster_means = new_cluster_means

    return assignment, cluster_means


def update_medoids(dissimilarity_matrix, indices):
    best_cost = 1.0e9
    best_index = -1

    cost = 0.0
    for current_index in indices:
        for other_index in indices:
            cost += dissimilarity_matrix[current_index][other_index]

        if best_cost > cost:
            best_cost = cost
            best_index = current_index

    return best_index


def kmedoids(dissimilarity_matrix, initial_cluster_means):
    assignment = dict()
    cluster_medoids = initial_cluster_means.copy()

    while True:
        # Assign the new vector to a cluster
        for i in range(500):
            best_cluster_id = -1
            best_distance = 1000000000.0

            for j in range(500):


            for k in range(10):
                dist = np.linalg.norm(X[i] - cluster_medoids[k])
                dist *= dist # squared Euclidean distance

                if best_distance > dist:
                    best_distance = dist
                    best_cluster_id = k

            assignment[i] = best_cluster_id

        # Update the cluster medoids
        new_cluster_medoids = np.zeros([10, len(initial_cluster_means[0])])

        # Try update the medoids
        # First, map each digit to the list of matrix indices
        digit_to_matrix_indices = dict()
        for i in range(500):
            if y[i] not in digit_to_matrix_indices:
                digit_to_matrix_indices[y[i]] = []

            digit_to_matrix_indices[y[i]].append(i)

        for digit in digit_to_matrix_indices.keys():
            matrix_indices = digit_to_matrix_indices[digit]
            best_index = update_medoids(dissimilarity_matrix, matrix_indices)
            new_cluster_medoids[digit] = X[best_index]

            pass

        if np.array_equal(new_cluster_medoids, cluster_medoids):
            break

        cluster_medoids = new_cluster_medoids

    return assignment, cluster_medoids


def compute_dissimilarity_matrix(data_matrix):
    n = len(data_matrix)
    dissimilarity_matrix = [[0 for i in range(n)] for j in range(n)]

    for y in range(n):
        for x in range(y + 1, n):
            dist = np.linalg.norm(data_matrix[y] - data_matrix[x])
            dissimilarity_matrix[y][x] = dist
            dissimilarity_matrix[x][y] = dist

    return dissimilarity_matrix


def visualize_digits(assignment, data_matrix):
    groups = [[] for i in range(10)]

    for i in range(len(data_matrix)):
        digit = assignment[i]
        groups[digit].append(data_matrix[i])

    for digit in range(len(groups)):
        print "Printing for digit", digit
        mnist.visualize(np.array(groups[digit]))


def main():
    Xin = X[0:500]

    print "=== k-means ==="

    assignment1, cluster_means1 = kmeans(Xin, X[0:10])

    print "= First iteration"
    print "Cluster means"
    mnist.visualize(cluster_means1)

    print "Clusters"

    visualize_digits(assignment1, Xin)

    print "= Second iteration"

    distinct_means = X[0:10].copy()
    digit_set = set()

    for i in range(len(Xin)):
        digit = y[i]

        if digit not in digit_set:
            digit_set.add(digit)
            distinct_means[digit] = Xin[i]

            if len(digit_set) == 10:
                break

    print digit_set

    assignment1, cluster_means1 = kmeans(Xin, distinct_means)
    print "Cluster means"
    mnist.visualize(cluster_means1)

    print "Clusters"
    visualize_digits(assignment1, Xin)

    print "=== k-medoids ==="
    dissimilarity_matrix = compute_dissimilarity_matrix(Xin)

    print "= First iteration"
    assignment2, cluster_medoids1 = kmedoids(dissimilarity_matrix, X[0:10])
    print "Cluster medoids"
    mnist.visualize(cluster_medoids1)

    print "Clusters"
    visualize_digits(assignment2, Xin)

    print "= Second iteration"

    assignment2, cluster_medoids1 = kmedoids(dissimilarity_matrix, distinct_means)
    print "Cluster medoids"
    mnist.visualize(cluster_medoids1)

    print "Clusters"
    visualize_digits(assignment2, Xin)


if __name__ == "__main__":
    main()
