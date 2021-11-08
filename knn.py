import math
import random
from dataclasses import dataclass

import pygame


@dataclass
class Point:
    x: int
    y: int
    cluster: int


cluster_map = {0: 'red', 1: 'blue', 2: 'green', -1: 'orange'}


def generateData(numberOfClassEl, numberOfClasses):
    data = []
    for classNum in range(numberOfClasses):
        # Choose random center of 2-dimensional gaussian
        centerX, centerY = random.randint(20, 580), random.randint(20, 380)
        # Choose numberOfClassEl random nodes with RMS=0.5
        for rowNum in range(numberOfClassEl):
            data.append(Point(random.gauss(centerX, 20), random.gauss(centerY, 20), classNum))
    return data


def draw_pygame(points):
    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    pygame.display.update()
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(points_validate) == 0 or points_validate[-1].cluster != -1:
                        points_validate.append(Point(event.pos[0], event.pos[1], -1))
            if event.type == pygame.KEYDOWN:
                if points_validate[-1].cluster == -1:
                    if event.key == pygame.K_1:
                        points_validate[-1].cluster = 0
                        kNN(points_validate[-1], 3)
                    if event.key == pygame.K_2:
                        points_validate[-1].cluster = 1
                        kNN(points_validate[-1], 3)
                    if event.key == pygame.K_3:
                        points_validate[-1].cluster = 2
                        kNN(points_validate[-1], 3)
            screen.fill('WHITE')
            for point in points:
                pygame.draw.circle(screen, cluster_map[point.cluster], (point.x, point.y), 3)
            for point in points_validate:
                pygame.draw.circle(screen, cluster_map[point.cluster], (point.x, point.y), 3)
            pygame.display.update()


def dist(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def kNN(k, point):
    sorted_points = points.sort(key=lambda p: dist(point, p))
    print(sorted_points)


if __name__ == '__main__':
    n, cl = 100, 3
    points = generateData(n, cl)
    points_validate = []
    draw_pygame(points)
