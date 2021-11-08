import random
from dataclasses import dataclass

import numpy as np
import pygame
from sklearn.svm import SVC


@dataclass
class Line:
    first_point: (int, int)
    last_point: (int, int)
    color: str


@dataclass
class Point:
    x: int
    y: int
    cluster: int


@dataclass
class PredictionLine:
    main: Line
    margin_above: Line
    margin_below: Line


cluster_map = {0: 'yellow', 1: 'green'}  # Заданные кластеры
model = SVC(kernel='linear')


def features_and_labels(dots: [Point]) -> (np.ndarray, np.ndarray):
    features = []
    labels = []
    for dot in dots:
        features.append([dot.x, dot.y])
        labels.append(dot.cluster)

    return np.array(features), np.array(labels)


def generateData(dots, clusters):
    data = []
    for classNum in range(clusters):
        centerX, centerY = random.randint(20, 580), random.randint(60, 380)
        for rowNum in range(dots):
            data.append(Point(random.gauss(centerX, 20), random.gauss(centerY, 20), classNum))
    return data


def draw_pygame(points, prediction_line_system: PredictionLine):
    pygame.font.init()
    screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
    pygame.display.update()
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    prediction = model.predict(np.array([[event.pos[0], event.pos[1]]]))
                    new_dot = Point(event.pos[0], event.pos[1], prediction[0])
                    points.append(new_dot)

            screen.fill('WHITE')
            for point in points:
                pygame.draw.circle(screen, cluster_map[point.cluster], (point.x, point.y), 3)
            pygame.draw.line(
                screen,
                prediction_line_system.main.color,
                prediction_line_system.main.first_point,
                prediction_line_system.main.last_point,
                2
            )
            pygame.draw.line(
                screen,
                prediction_line_system.margin_above.color,
                prediction_line_system.margin_above.first_point,
                prediction_line_system.margin_above.last_point
            )
            pygame.draw.line(
                screen,
                prediction_line_system.margin_below.color,
                prediction_line_system.margin_below.first_point,
                prediction_line_system.margin_below.last_point
            )

            pygame.display.update()


if __name__ == '__main__':
    n, cl = 100, 2
    points = generateData(n, cl)

    X, y = features_and_labels(points)
    model.fit(X, y)
    w = model.coef_[0]
    b = model.intercept_[0]
    x_points = np.linspace(0, 800, num=2)
    y_points = -(w[0] / w[1]) * x_points - b / w[1]

    unit_normal_vector = model.coef_[0] / (np.sqrt(np.sum(model.coef_[0] ** 2)))
    margin = 1 / np.sqrt(np.sum(model.coef_[0] ** 2))

    main_points = np.array(list(zip(x_points, y_points)))
    points_of_line_above = main_points + unit_normal_vector * margin
    points_of_line_below = main_points - unit_normal_vector * margin

    line_system = PredictionLine(
        main=Line(
            first_point=(main_points[0][0], main_points[0][1]),
            last_point=(main_points[1][0], main_points[1][1]),
            color='pink'
        ),
        margin_above=Line(
            first_point=(points_of_line_above[0][0], points_of_line_above[0][1]),
            last_point=(points_of_line_above[1][0], points_of_line_above[1][1]),
            color='black'
        ),
        margin_below=Line(
            first_point=(points_of_line_below[0][0], points_of_line_below[0][1]),
            last_point=(points_of_line_below[1][0], points_of_line_below[1][1]),
            color='black'
        )
    )

    draw_pygame(points, line_system)
