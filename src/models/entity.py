from abc import ABC
from models.game_board import GameBoard
from util.util import find_degree_of_movement, find_closest_entity, find_distance


class Entity(ABC):

    def __init__(self, pixel_locations, board: GameBoard, previous_entity=None):
        """
        :param pixel_locations: [x,y] locations
        """
        self.xy_positions = pixel_locations
        self.frame = board.frame

        self.x_high, self.x_low, self.y_high, self.y_low = 0, 1000, 0, 1000

        if isinstance(self, Missile):
            # If this is a missile, only use the first x, y coord set
            x, y = self.xy_positions[0]
            self.x_high, self.x_low, self.x_center = x, x, x
            self.y_high, self.y_low, self.y_center = y, y, y
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
            self.calculate_velocity(previous_entity)
        board.register_entity(self)

    def get_area(self) -> int:
        return len(self.xy_positions)

    def calculate_velocity(self, previous_entity):
        """
        Calculate the entities speed and direction
        :return: None, self.velocity_magnitude and self.velocity_direction get set
        """
        if previous_entity:
            x1, y1 = previous_entity.x_center, previous_entity.y_center
            x2, y2 = self.x_center, self.y_center

            if x1 == x2 and y1 == y2:
                # Leave the direction as None and the magnitude as 0 if the entity hasn't moved
                self.velocity_magnitude = 0
            else:
                # Find the direction of the moving entity by finding the degree of the line that is drawn
                self.velocity_direction = find_degree_of_movement(x1, y1, x2, y2)
                distance = find_distance(x1, y1, x2, y2)
                self.velocity_magnitude = distance / (self.frame - previous_entity.frame)

    def __str__(self):
        return f'\n\tArea: {self.get_area()}' \
            f'\n\tX low, high: {self.x_low}, {self.x_high}' \
            f'\n\tY low, high: {self.y_low}, {self.y_high}' \
            f'\n\tVel Mag: {self.velocity_magnitude}' \
            f'\n\tVel Dir: {self.velocity_direction}'


class Ship(Entity):
    TURNING_SPEED = 360 / 45

    @staticmethod
    def create_ship(x: int, y: int, board: GameBoard):
        pixel_locations = board.gather_connecting_pixels(x, y)

        if len(pixel_locations) <= 15:
            # Unexplore the locations if it was a red missile
            for x, y in pixel_locations:
                board.explored_mapping[x][y] = False
            return None
        else:
            return Ship(pixel_locations, board)

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
                if len(degrees_for_ship_tips):
                    self.ship_tip = \
                        potential_ship_tips[degrees_for_ship_tips.index(min(degrees_for_ship_tips, key=abs))]
            else:
                # Otherwise pick the first potential_ship_tip in the list and hope for the best
                self.ship_tip = potential_ship_tips[0]

        if self.ship_tip is None:
            self.ship_tip = self.xy_positions[0]
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

        return find_degree_of_movement(x1, y1, x2, y2)

    def __str__(self):
        return f'Ship ({self.x_center}, {self.y_center}):\n\tDEG {self.direction_deg}' \
            f'\n\tShip Tip: {self.ship_tip} ' \
            f'{super().__str__()}'


class Asteroid(Entity):
    """
    Entity to represent an Asteroid of a single color
    """

    @staticmethod
    def create_asteroid(x: int, y: int, board: GameBoard):
        """
        Create an asteroid given one of it's locations and the game board, this uses a basic search
        algorithm to determine all the locations the asteroid occupies
        :return: built Asteroid
        """
        pixel_locations = board.gather_connecting_pixels(x, y)
        return Asteroid(pixel_locations, board)

    def __init__(self, pixel_locations, board: GameBoard, transposed=False):
        super().__init__(pixel_locations, board)
        self.transposed = transposed
        previous_asteroid = find_closest_entity(self, board.get_last_asteroids())
        self.calculate_velocity(previous_asteroid)

    def __str__(self):
        return f'Asteroid ({self.x_center}, {self.y_center}): {super().__str__()}'


class Missile(Entity):
    """
    Entity to represent the missile that gets shot out of the Ship
    """
    RED_MISSILE = 0
    BLUE_MISSILE = 1
    # Speed determined experimentally
    SPEED = 3.1622

    def __init__(self, pixel_locations, board: GameBoard):
        # Determine if this is the red missile or the blue missile
        x, y = pixel_locations[0]
        if board.check_pixel(x, y, GameBoard.RED_MISSILE_RGB):
            self.missile_type = Missile.RED_MISSILE
        else:
            self.missile_type = Missile.BLUE_MISSILE
        last_missile = board.get_last_missile(self.missile_type)
        super().__init__(pixel_locations, board, last_missile)

    def __str__(self):
        missile_type = 'Red' if self.missile_type == Missile.RED_MISSILE else 'Blue'
        return f'{missile_type} Missile ({self.x_center}, {self.y_center}): {super().__str__()}'
