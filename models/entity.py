from abc import ABC
from models.game_board import GameBoard
from util import find_degree_of_line, find_closest_entity, find_distance


class Entity(ABC):

    def __init__(self, pixel_locations, board: GameBoard, previous_entity=None):
        """
        :param pixel_locations: [x,y] locations
        """
        self.xy_positions = pixel_locations
        self.frame = board.frame

        self.x_high, self.x_low, self.y_high, self.y_low = 0, 1000, 0, 1000

        if len(self.xy_positions) == 1:
            # If the entity is only 1 pixel, set the high, low,
            # and center values to be the same as the one pixel
            x, y = self.xy_positions[0]
            self.x_high, self.x_low, self.x_center = x
            self.y_high, self.y_low, self.y_center = y
        else:
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

        self.velocity_direction = None
        self.velocity_magnitude = None
        if previous_entity:
            x1, y1 = previous_entity.x_center, previous_entity.y_center
            x2, y2 = self.x_center, self.y_center

            if x1 == x2 and y1 == y2:
                # Leave the direction as None and the magnitude as 0 if the entity hasn't moved
                self.velocity_magnitude = 0
            else:
                # Find the direction of the moving entity by finding the degree of the line that is drawn
                self.velocity_direction = find_degree_of_line(x1, y1, x2, y2)
                distance = find_distance(x1, y1, x2, y2)
                self.velocity_magnitude = distance / (board.frame - previous_entity.frame)

        board.register_entity(self)


class Ship(Entity):

    def __init__(self, pixel_locations, board: GameBoard):
        """
        :param pixel_locations: [x,y] locations
        """
        previous_ship = board.get_last_ship()
        super().__init__(pixel_locations, board, previous_entity=previous_ship)

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

    def find_deg_angle_of_ship_tip(self, ship_tip):
        """
        Determine the degree of the ship
        :param ship_tip: x,y coord of the tip of the ship
        :return: degree from 0-359 degrees
        """
        # Find the equation of the line from the center point to the tip of the ship
        x1, y1 = ship_tip
        x2, y2 = self.x_center, self.y_center

        return find_degree_of_line(x1, y1, x2, y2)


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
        return Asteroid(pixel_locations, board)

    def __init__(self, pixel_locations, board: GameBoard):
        super().__init__(pixel_locations, board)
        previous_asteroid = find_closest_entity(self, board.get_last_asteroids())
        # Reinit the object since we have the previous asteroid now
        super().__init__(pixel_locations, board, previous_entity=previous_asteroid)
        self.RGB_vals = pixel_locations[0]

    def _get_area(self):
        return len(self.xy_positions)

    def __str__(self):
        return f'Asteroid ({self.x_center}, {self.y_center}): Area = {self._get_area()}'


class Missile(Entity):

    def __init__(self, pixel_locations, board: GameBoard):
        last_missile = board.get_last_missile()
        super().__init__(pixel_locations, board, previous_entity=last_missile)

    def __str__(self):
        return f'Missile ({self.x_center}, {self.y_center}): ' \
            f'\n\tVelocity Direction: {self.velocity_direction}' \
            f'\n\tVelocity Magnitude: {self.velocity_magnitude}'
