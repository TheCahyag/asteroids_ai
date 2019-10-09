from abc import ABC, abstractmethod

from models.entity import Ship, Asteroid
from models.game_board import GameBoard
from util import print_board


class AbstractAgent(ABC):

    def __init__(self, action_space):
        self.action_space = action_space
        self.frame = 0
        self.board = None

    @abstractmethod
    def act(self, observation, reward: int, done: bool) -> int:
        self.board = GameBoard(observation, self.frame)

        # Keep track of the pixel for the ship
        ship_pixels = []

        x, y = 0, 0

        print_board(self.board)

        # Look through the game board to find the ship and/or asteroids
        while x < len(observation):
            while y < len(observation[0]):
                if not self.board.is_location_explored(x, y):
                    if self.board.check_pixel(x, y, GameBoard.BLANK_RGB):
                        # Skip blank pixels
                        pass
                    elif self.board.check_pixel(x, y, GameBoard.SHIP_RGB):
                        ship_pixels.append([x, y])
                    elif self.board.check_pixel(x, y, GameBoard.MISSILE_RGB):
                        pass
                    elif self.board.check_pixel(x, y, GameBoard.GAME_OBJECTS):
                        # Score board and lives left
                        pass
                    else:
                        Asteroid.create_asteroid(x, y, self.board)

                    self.board.explore_location(x, y)
                y += 1
            x += 1
            y = 0

        if len(ship_pixels) is not 0:
            Ship(ship_pixels, self.board)

