import numpy as np
import matplotlib.pyplot as plt


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


def main():
    x_coordinates = get_x_coordinates()

    for k in range(0, 11):
        process(x_coordinates, k)


if __name__ == "__main__":
    main()
