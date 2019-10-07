import math
from abc import ABC, abstractmethod
from models.game_board import GameBoard


class Entity(ABC):

    def __init__(self, pixel_locations):
        """
        :param pixel_locations: [x,y] locations
        """
        self.xy_positions = pixel_locations

        self.x_high, self.x_low, self.y_high, self.y_low = 0, 1000, 0, 1000
        self.movement_direction = None

        # Get the highest and lowest x and y values for the entity
        for x, y in self.xy_positions:
            if x > self.x_high:
                self.x_high = x
            elif x < self.x_low:
                self.x_low = x
            if y > self.y_high:
                self.y_high = y
            elif y < self.y_low:
                self.y_low = y

        # Set the X,Y location of the center of the entity
        self.x_center = (self.x_high + self.x_low) / 2
        self.y_center = (self.y_high + self.y_low) / 2
        print(f'Center: {self.x_center}, {self.y_center}, {self.__class__}')

    @abstractmethod
    def set_movement_direction(self, board: GameBoard):
        pass


class Ship(Entity):

    def __init__(self, pixel_locations, previous_ship=None):
        """
        :param pixel_locations: [x,y] locations
        :param previous_ship: Ship object representing the last position of the ship
        """
        super().__init__(pixel_locations)

        self.ship_tip = None

        potential_ship_tips = []

        # Find the tip of the ship for determining the direction
        for x, y in self.xy_positions:
                m, n = -1, -1
                neighbors = 0
                while m <= 1:
                    while n <= 1:
                        x_mod = x + m
                        y_mod = y + n
                        if x == x_mod and y == y_mod:
                            # Skip the point we are looking at
                            break
                        if [x_mod, y_mod] in self.xy_positions:
                            neighbors += 1
                        n += 1
                    m += 1
                    n = -1
                if neighbors == 1:
                    potential_ship_tips.append([x, y])
        if len(potential_ship_tips) == 1:
            self.ship_tip = potential_ship_tips[0]
        else:
            if previous_ship is not None:
                # If we have the data from the previous ship, calculate all the degree
                # positions and choose the one that is closest to that of the previous ship
                degrees_for_ship_tips = []
                for potential_ship_tip in potential_ship_tips:
                    degrees_for_ship_tips.append(self.find_deg_angle_of_ship_tip(potential_ship_tip))
                degrees_for_ship_tips[:] = [x - previous_ship.direction_deg for x in degrees_for_ship_tips]
                self.ship_tip = potential_ship_tips[degrees_for_ship_tips.index(min(degrees_for_ship_tips, key=abs))]

            else:
                # Otherwise pick the first potential_ship_tip in the list and hope for the best
                self.ship_tip = potential_ship_tips[0]

        assert self.ship_tip is not None
        self.direction_deg = self.find_deg_angle_of_ship_tip(self.ship_tip)

        print(f'DEG: {self.direction_deg}')

    def set_movement_direction(self, board: GameBoard):
        pass

    def find_deg_angle_of_ship_tip(self, ship_tip):
        """
        Determine the degree of the ship
        :param ship_tip: x,y coord of the tip of the ship
        :return: degree from 0-359 degrees
        """
        # Find the equation of the line from the center point to the tip of the ship
        x1, y1 = ship_tip
        x2, y2 = self.x_center, self.y_center

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


class Asteroid(Entity):

    @staticmethod
    def create_asteroid(x: int, y: int, board: GameBoard):
        """
        Create an asteroid given one of it's locations and the game board
        :return: built Asteroid
        """
        pixel_locations = []
        new_pixels = [[x, y]]
        while len(new_pixels) > 0:
            x_pos, y_pos = new_pixels.pop()
            pixel_locations.append([x_pos, y_pos])

            i, j = -1, -1
            while i <= 1:
                while j <= 1:
                    x_cur = x_pos + i
                    y_cur = y_pos + j
                    if x_cur == x_pos and y_cur == y_pos:
                        j += 1
                        continue
                    else:
                        if not board.is_location_explored(x_cur, y_cur) \
                                and [x_cur, y_cur] not in pixel_locations \
                                and [x_cur, y_cur] not in new_pixels \
                                and board.check_pixel(x_cur, y_cur, board.game_map[x][y]):
                            # Only look at the position if it hasn't been explored yet
                            # and it isn't already in our pixel location set
                            # and it isn't already in our new pixel array
                            # and the position has the same RBG values as the original location given
                            new_pixels.append([x_cur, y_cur])
                            board.explore_location(x_cur, y_cur)
                    j += 1
                i += 1
                j = -1
            # Remove duplicates and return as list
        a = Asteroid(pixel_locations)
        print(a)
        return a

    def __init__(self, pixel_locations):
        super().__init__(pixel_locations)
        self.RGB_vals = pixel_locations[0]

    def set_movement_direction(self, board: GameBoard):
        pass

    def _get_area(self):
        return len(self.xy_positions)

    def __str__(self):
        return f'Asteroid ({self.x_center}, {self.y_center}): Area = {self._get_area()}'