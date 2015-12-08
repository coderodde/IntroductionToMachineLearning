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


def main():
    Xin = X[0:500]
    assignment1, cluster_means1 = kmeans(Xin, X[0:10])

    for mean in cluster_means1:
        mnist.visualize(mean)

    distinct_means = X[0:10].copy()
    digit_set = set()

    for i in range(len(Xin)):
        digit = y[i]

        if digit not in digit_set:
            digit_set.add(digit)
            distinct_means[digit] = Xin[i]

            if len(digit_set) == 10:
                break

    assignment2, cluster_means2 = kmeans(Xin, distinct_means)

    for mean in cluster_means2:
        mnist.visualize(mean)

if __name__ == "__main__":
    main()