import math


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
