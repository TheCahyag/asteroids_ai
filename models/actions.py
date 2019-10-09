import enum


class AsteroidsActions(enum.Enum):
    DO_NOTHING = 0
    MOVE_FORWARD = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    FIRE_MOVE_FORWARD = 8
    FIRE_TURN_RIGHT = 9
    FIRE_TURN_LEFT = 10
