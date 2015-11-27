import numpy as np
import matplotlib.pyplot as plt
import random

def get_x_coordinates():
    return 6.0 * np.random.random_sample(30) - 3.0


def f_raw(x):
    return 2 + x - 0.5 * (x ** 2)


def f(x):
    return f_raw(x) + np.random.normal(0.0, 0.4)


def get_y_coordinates(x_coordinates):
    arr = []

    for x in x_coordinates:
        arr.append(f(x))

    return np.array(arr)


def det_coef(sampled_values, fitted_values):
    ave = np.mean(sampled_values)
    upper_sum = 0
    lower_sum = 0

    for i in range(0, len(sampled_values)):
        upper_sum += (sampled_values[i] - fitted_values[i]) ** 2
        lower_sum += (sampled_values[i] - ave) ** 2

    return upper_sum / lower_sum


def process(x_coordinates, k):
    space = np.linspace(-3.0, 3.0, 1000)
    y_coordinates = get_y_coordinates(x_coordinates)
    p = np.polyfit(x_coordinates, y_coordinates, k)
    v = np.polyval(p, space)
    plt.plot(x_coordinates, f(x_coordinates), 'ro')
    plt.plot(space, v)
    plt.axis([-3, 3, -6, 4])
    plt.title('K = ' + str(k) + ", R^2 = " + str(det_coef(y_coordinates, np.polyval(p, x_coordinates))))
    plt.show()


def task_a():
    x_coordinates = get_x_coordinates()

    for k in range(0, 10):
        process(x_coordinates, k)


def cross_validate(x_coord_chunks, skip_chunk_id, k):
    x_coords = []
    x_target_coords = []

    for i in range(0, 10):
        if i != skip_chunk_id:
            x_coords.extend(x_coord_chunks[i])
        else:
            x_target_coords.extend(x_coord_chunks[i])

    y_coords = get_y_coordinates(x_coords)
    p = np.polyfit(x_coords, y_coords, k)
    y_target_coords = get_y_coordinates(x_target_coords)

    err = 0

    for i in range(0, 3):
        err += (y_target_coords[i] - np.polyval(p, x_target_coords[i])) ** 2

    return err


def task_b():
    x_coords = get_x_coordinates()
    random.shuffle(x_coords)
    x_coord_chunks = []

    for i in range(0, len(x_coords), 3):
        chunk = []

        for j in range(i, i + 3):
            chunk.append(x_coords[j])

        x_coord_chunks.append(chunk)

    for k in range(0, 11):
        for skip_chunk_id in range(0, 10):
            error = cross_validate(x_coord_chunks, skip_chunk_id, k)
            print "K = " + str(k) + ", j = " + str(skip_chunk_id) + ", squared error = " + str(error)


def main():
    #task_a()
    task_b()


if __name__ == "__main__":
    main()
