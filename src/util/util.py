import math
import numpy as np


def find_closest_entity(entity, entities, threshold=5):
    """
    Find the entity in entities that is closest to entity
    :param entity: target entity
    :param entities: list of entities to search through
    :param threshold: if the distance is greater than this value they are too far away
    :return: The closest Entity or None
    """
    import models.entity as en

    closest: en.Entity = None
    for e in entities:
        x1, y1 = entity.x_center, entity.y_center
        x2, y2 = e.x_center, e.y_center
        d = find_distance(x1, y1, x2, y2)
        if d <= threshold:
            if closest is None:
                closest = e
            else:
                closest = e if d < find_distance(x1, y1, closest.x_center, closest.y_center) else closest
    return closest


def find_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_degree_of_movement(x1, y1, x2, y2):
    """
    Find the degree of the line in a unit circle where x2,y2 is the origin and x1,y1 is the point on the circle
    """
    x_diff = x2 - x1
    y_diff = y1 - y2

    x1, y1 = x2 + y_diff, y2 + x_diff

    radius = find_distance(x1, y1, x2, y2)

    x_diff = x2 - x1
    y_diff = y2 - y1

    # Get the edge cases
    if x_diff == 0:
        if y_diff > 0:
            return 270
        elif y_diff < 0:
            return 90
    elif y_diff == 0:
        if x_diff > 0:
            return 180
        elif x_diff < 0:
            return 0

    angle_rad = math.sin(abs(x_diff) / radius)
    angle = (angle_rad * 180) / math.pi

    # Quad 1
    if x_diff < 0 and y_diff < 0:
        if find_distance(x1, y1, x2, y1) <= find_distance(x1, y1, x1, y2):
            # The point is closer to quad 2
            return 90 - angle
        else:
            # The point is closer to quad 4
            return angle
    # Quad 2
    elif x_diff > 0 and y_diff < 0:
        if find_distance(x1, y1, x2, y1) <= find_distance(x1, y1, x1, y2):
            # The point is closer to quad 1
            return 90 + angle
        else:
            # The point is closer to quad 3
            return 180 - angle
    # Quad 3
    elif x_diff > 0 and y_diff > 0:
        if find_distance(x1, y1, x2, y1) <= find_distance(x1, y1, x1, y2):
            # The point is closer to quad 2
            return 180 + angle
        else:
            # The point is closer to quad 4
            return 270 - angle
    # Quad 4
    elif x_diff < 0 and y_diff > 0:
        if find_distance(x1, y1, x2, y1) <= find_distance(x1, y1, x1, y2):
            # The point is closer to quad 3
            return 270 + angle
        else:
            # The point is closer to quad 1
            return 360 - angle


def x_y_split_based_on_angle(angle: float) -> (float, float):
    if angle == 0 or angle == 360:
        return 1, 0
    elif angle == 90:
        return 0, -1
    elif angle == 180:
        return -1, 0
    elif angle == 270:
        return 0, 1

    # Quad 1
    if 0 < angle < 90:
        return ((90 - (angle % 90)) / 90), -(angle % 90 / 90)
    # Quad 2
    elif 90 < angle < 180:
        return -(angle % 90 / 90), -((90 - (angle % 90)) / 90)
    # Quad 3
    elif 180 < angle < 270:
        return -((90 - (angle % 90)) / 90), (angle % 90 / 90)
    # Quad 4
    elif 270 < angle < 360:
        return (angle % 90 / 90), ((90 - (angle % 90)) / 90)


def matrix_add_vector(matrix, vector):
    """
    Matrix should be in the form of
    [
        [x1, y1],
        [x2, y2],
        [xn, yn]
    ]
    Vector should be in the form of
    [
        x
        y
    ]
    :return: A 2D array (following the same format as received) of xy coordinates
    """
    # Mold the matrix into a 2 row matrix
    xs = []
    ys = []
    for array in matrix:
        xs.append(array[0])
        ys.append(array[1])
    m = np.array([xs, ys])
    v = np.array([[vector[0]], [vector[1]]])

    m_mod = m + v

    return_array = []
    i = 0
    while i < len(m_mod[0][0]):
        return_array.append([m_mod[0][0][i], m_mod[1][0][i]])
        i += 1
    return return_array
