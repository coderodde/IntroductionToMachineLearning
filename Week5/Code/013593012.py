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

def main():
    x_coordinates = get_x_coordinates()
    p = np.polyfit(x_coordinates, get_y_coordinates(x_coordinates), 10)
    v = np.polyval(p, np.linspace(-3.0, 3.0, 1000))
    plt.plot(x_coordinates, f(x_coordinates), 'ro')
    plt.plot(np.linspace(-3.0, 3.0, 1000), v)
    plt.axis([-3, 3, -6, 3])
    plt.show()

if __name__ == "__main__":
    main()
