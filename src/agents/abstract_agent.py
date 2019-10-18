from abc import ABC, abstractmethod

from models.entity import Ship, Asteroid, Missile
from models.game_board import GameBoard


class AbstractAgent(ABC):

    def __init__(self, action_space):
        self.action_space = action_space
        self.frame = 0
        self.board: GameBoard = None

    @abstractmethod
    def act(self, observation, reward: int, done: bool) -> int:
        self.board = GameBoard(observation, self.frame)

        # Keep track of the pixel for the ship
        blue_missile_pixels = []
        red_missile_pixels = []

        x, y = 0, 0

        # Look through the game board to find the ship and/or asteroids
        while x < len(observation):
            while y < len(observation[0]):
                if not self.board.is_location_explored(x, y):
                    if sum(self.board.game_map[x][y]) == 0:
                        # Skip blank pixels
                        pass
                    elif self.board.check_pixel(x, y, GameBoard.SHIP_RGB):
                        ship = Ship.create_ship(x, y, self.board)
                        if ship is None:
                            red_missile_pixels.append([x, y])
                    elif self.board.check_pixel(x, y, GameBoard.BLUE_MISSILE_RGB):
                        blue_missile_pixels.append([x, y])
                    elif self.board.check_pixel(x, y, GameBoard.SCORE_RGB):
                        # Score board and lives left
                        pass
                    else:
                        # If the pixel hasn't been recognized yet then it's an asteroid
                        Asteroid.create_asteroid(x, y, self.board)

                    self.board.explore_location(x, y)
                y += 1
            x += 1
            y = 0

        # Construct the blue missile, if present
        if len(blue_missile_pixels) is not 0:
            Missile(blue_missile_pixels, self.board)
        # Construct the red missile, if present
        if len(red_missile_pixels) is not 0:
            Missile(red_missile_pixels, self.board)
