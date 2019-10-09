import math

from models.entity import Entity
from models.game_board import GameBoard


def print_board(board: GameBoard):
    string = ''
    x, y = 0, 0
    while x < len(board.game_map):
        while y < len(board.game_map[0]):
            if board.check_pixel(x, y, GameBoard.BLANK_RGB):
                string = string + '.'
            else:
                string = string + 'x'
            y += 1
        x += 1
        y = 0
        string = string + '\n'
    print(string)


def find_closest_entity(entity: Entity, entities: [Entity], threshold=5) -> Entity:
    """
    Find the entity in entities that is closest to entity
    :param entity: target entity
    :param entities: list of entities to search through
    :param threshold: if the distance is greater than this value they are too far away
    :return: The closest Entity or None
    """
    closest: Entity = None
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


def find_degree_of_line(x1, y1, x2, y2):
    x_diff = x2 - x1
    y_diff = y2 - y1
    m = None
    try:
        m = -(y_diff / x_diff)
    except ZeroDivisionError:
        pass

    if m is None or m == 0:
        if x_diff < 0:
            degree = 180
        else:
            degree = 0
    else:
        c = math.sqrt(abs(x_diff) ** 2 + abs(y_diff) ** 2)
        degree = 180 * math.asin(abs(x_diff) / c) / math.pi
    return degree
