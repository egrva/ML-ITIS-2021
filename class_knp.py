import matplotlib.pyplot as plt
import numpy as np
import time


def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def weight():
    r = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            r[i][j] = dist(points[i], points[j])
    return r


def random_points():
    x = np.random.randint(0, 100, n)
    y = np.random.randint(0, 100, n)
    return [x, y]


def minimum_length():
    minim = np.inf
    i_min, j_min = -1, -1
    for i in range(n):
        for j in range(i + 1, n):
            if minim > weights[i][j]:
                minim = weights[i][j]
                i_min, j_min = i, j
    connections[i_min][j_min] = connections[j_min][i_min] = 1
    connections[i_min][i_min] = connections[j_min][j_min] = -1


def link():
    minim = np.inf
    i_min, j_min = -1, -1
    for i in range(n):
        if connections[i][i] == -1:
            for j in range(n):
                if connections[j][j] == 0:
                    if minim > weights[i][j]:
                        minim = weights[i][j]
                        i_min, j_min = i, j
    connections[i_min][j_min] = connections[j_min][i_min] = 1
    connections[j_min][j_min] = -1


if __name__ == '__main__':
    n = 10
    points = []
    for i in range(n):
        points.append((random_points()[0][i],
                       random_points()[1][i]))
    weights = weight()
    connections = np.zeros((n, n))
    # for i in range(n):
    # plt.scatter(points[i][0], points[i][1])
    minimum_length()
    for k in range(n - 1):
        for i in range(n):
            plt.scatter(points[i][0], points[i][1])
        for i in range(n):
            for j in range(i + 1, n):
                if connections[i][j] == 1:
                    plt.plot((points[i][0], points[j][0]),
                             (points[i][1], points[j][1]))
        link()
        plt.show()
        time.sleep(1)
    plt.show()
