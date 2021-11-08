import math

import numpy as np
from matplotlib import pyplot as plt, colors


class Dot:
    """Класс точки"""

    def __init__(self, x, y, cluster=None):
        self.x = x
        self.y = y
        self.cluster = cluster

    def get_distance(self, other_dot):
        """Расчет расстояния между точками"""
        return math.sqrt(
            (self.x - other_dot.x) ** 2 + (self.y - other_dot.y) ** 2
        )

    def __eq__(self, other):
        if isinstance(other, list):
            return self in other
        else:
            return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def create_random_dot(min_v, max_v, cluster=None):
    return Dot(
        np.random.randint(min_v, max_v),
        np.random.randint(min_v, max_v),
        cluster
    )


def create_random_dots(min_v=1, max_v=100, count=100, cluster=None):
    dots = [create_random_dot(min_v, max_v, cluster) for i in range(count)]
    return dots


def get_dots_position_lists(dots):
    x = []
    y = []
    for dot in dots:
        x.append(dot.x)
        y.append(dot.y)
    return x, y


def show_clusters_picture(cluster, filename='clusters_picture.png'):
    fig, ax = plt.subplots()
    for index, (center, dots) in enumerate(cluster.items()):
        x, y = get_dots_position_lists(dots)
        ax.scatter(x, y, edgecolors=list(colors.cnames.keys())[index])
    fig.savefig(filename)
    plt.show()
