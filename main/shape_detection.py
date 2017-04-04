from rdp import rdp
import numpy as np
import cv2


def _align_points(points):
    if points.shape[0] > 0 and points.shape[1] == 2:
        x = points[0][0]
        y = points[0][1]
        for point in points :
            if point[0] < x:
                x = point[0]
            if point[1] < y:
                y = point[1]
        for i in range(len(points)):
            points[i][0] -= x
            points[i][1] -= y
        return points
    else:
        raise ValueError('Array must have [Nx2] shape')


def _rdp_reduction(points):
    scale = points[0][0]
    for point in points:
        if point[0] > scale:
            scale = point[0]
        if point[1] > scale:
            scale = point[1]
    reduced = rdp(points, scale / 100)
    if reduced.shape[0] == 2 and np.array_equal(reduced[0], reduced[1]):
        return np.array([reduced[0]])
    else:
        return reduced


def _angle_between(vector_1, vector_2):
    vector_1 = vector_1 / np.linalg.norm(vector_1)
    vector_2 = vector_2 / np.linalg.norm(vector_2)
    return np.arccos(np.clip(np.dot(vector_1, vector_2), -1.0, 1.0))


def _angles(points):
    if len(points) >= 3:
        angles = []
        for i in range(len(points) - 1):
            angles.append(_angle_between(points[i] - points[i + 1], points[i] - points[i - 1]))
        angles.append(_angle_between(points[len(points) - 1] - points[0],
                                     points[len(points) - 1] - points[len(points) - 2]))
        return angles
    raise ValueError('There must be at least 3 points to calculate angles.')


def _edges(points):
    if len(points) >= 2:
        edges = []
        for i in range(len(points)):
            edges.append(np.linalg.norm(points[i] - points[i - 1]))
        return edges
    raise ValueError('There must be at least 2 points to calculate edges.')


def detect_shape(points):
    points = _rdp_reduction(_align_points(points))
    epsilon = points[0][0]
    for point in points:
        if point[0] > epsilon:
            epsilon = point[0]
        if point[1] > epsilon:
            epsilon = point[1]
    epsilon = epsilon / 100.0
    if len(points) == 1:
        return 'point'
    elif len(points) == 2:
        return 'line'
    elif len(points) == 3:
        angles = _angles(points)
        if abs(angles[0] - angles[1]) < np.pi / 50:
            if abs(angles[0] - angles[2]) < np.pi / 50:
                return 'equilateral triangle'
            else:
                return 'isosceles triangle'
        else:
            return 'triangle'
    elif len(points) == 4:
        angles = _angles(points)
        edges = _edges(points)
        if abs(angles[0] - np.deg2rad(90)) < np.pi / 50 and abs(angles[1] - np.deg2rad(90)) < np.pi / 50 and abs(
                        angles[2] - np.deg2rad(90)) < np.pi / 50 and abs(angles[3] - np.deg2rad(90)) < np.pi / 50:
            if abs(edges[0] - edges[1]) < epsilon and abs(edges[0] - edges[2]) < epsilon and abs(
                            edges[0] - edges[3]) < epsilon:
                return 'square'
            else:
                return 'rectangle'
        elif abs(angles[0] - angles[2]) < np.pi / 50 and abs(angles[1] - angles[3]) < np.pi / 50:
            if abs(edges[0] - edges[1]) < epsilon and abs(edges[0] - edges[2]) < epsilon and abs(
                            edges[0] - edges[3]) < epsilon:
                return 'rhombus'
            else:
                return 'parallelogram'
        elif abs(angles[0] + angles[1] - np.pi) < np.pi / 50 or abs(angles[1] + angles[2] - np.pi) < np.pi / 50 or abs(
                            angles[2] + angles[3] - np.pi) < np.pi / 50 or abs(
                            angles[3] + angles[0] - np.pi) < np.pi / 50:
            return 'trapezium'
        elif (abs(edges[0] - edges[1]) < epsilon and abs(edges[2] - edges[3]) < epsilon) or (abs(
                    edges[1] - edges[2]) < epsilon and abs(edges[3] - edges[0]) < epsilon):
            return 'kite'
        else:
            return 'quadrilateral'
    elif len(points) == 5:
        return 'pentagon'
    elif len(points) == 6:
        return 'hexagon'
    elif len(points) == 7:
        return 'heptagon'
    elif len(points) == 8:
        return 'octagon'
    elif len(points) >= 9:
        int_points = []
        for point in points:
            int_points.append([int(point[0] * 100), int(point[1] * 100)])
        ellipse = cv2.fitEllipse(np.array(int_points))
        ellipse = (
            (ellipse[0][0] / 100.0, ellipse[0][1] / 100.0), (ellipse[1][0] / 100.0, ellipse[1][1] / 100.0), ellipse[2])
        fit = 0
        for point in points:
            pos_x = (point[0] - ellipse[0][0]) * np.cos(-ellipse[2]) - (point[1] - ellipse[0][1]) * np.sin(-ellipse[2])
            pos_y = (point[0] - ellipse[0][0]) * np.sin(-ellipse[2]) - (point[1] - ellipse[0][1]) * np.cos(-ellipse[2])
            fit += abs((pos_x/ellipse[1][0])*(pos_x/ellipse[1][0]) + (pos_y/ellipse[1][1])*(pos_y/ellipse[1][1]) - 0.25)
        fit /= len(points)
        if fit < epsilon:
            if abs(ellipse[1][0] - ellipse[1][1]) < epsilon * 2:
                return 'circle'
            else:
                return 'ellipse'
        else:
            return 'polygon'
    else:
        return 'invalid'
