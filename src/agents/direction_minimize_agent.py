from agents.abstract_agent import AbstractAgent
from models.actions import AsteroidsActions
from models.entity import Asteroid, Missile, Ship
from util.util import find_distance, find_degree_of_movement, x_y_split_based_on_angle, matrix_add_vector


class DegreeMinimizing(AbstractAgent):
    """
    Shoot the asteroid that would require the least amount of turning first
    """

    def __init__(self, action_space):
        super().__init__(action_space)
        self.last_action = None
        self.last_target: Asteroid = None
        self.target: Asteroid = None
        self.target_angle = None
        self.angle_tolerance = 20
        self.currently_shooting = False

    def act(self, observation, reward: int, done: bool) -> int:
        # This processes the data from the observation
        super().act(observation, reward, done)
        self.frame += 1
        if done:
            return AsteroidsActions.DO_NOTHING.value
        if self.currently_shooting:
            if len(self.board.current_missiles) == 0:
                # No missiles have fired yet
                return AsteroidsActions.FIRE.value
            else:
                # A missile has fired and we can continue now
                self.currently_shooting = False

        # Get the most current ship
        ship = self.board.ship if self.board.ship else self.board.get_last_ship()
        if ship is None:
            return AsteroidsActions.DO_NOTHING.value

        # If there is no target find one only if the ship has been located
        if self.target is None:
            # Get the most current asteroids
            asteroids: [Asteroid] = self.board.asteroids \
                if len(self.board.asteroids) > 0 else self.board.get_last_asteroids()

            # Find the asteroid closest to the ship that's no less than 140 pixels away
            closest_asteroid, angle_diff = None, 360
            for asteroid in asteroids:
                # if self.last_target is not None:
                    # degree_from_last_target = find_degree_of_movement(self.last_target.x_center,
                    #                                                   self.last_target.y_center,
                    #                                                   ship.x_center, ship.y_center)
                    # # print(f'Distance from last target: {distance_from_last_target}')
                    # if distance_from_last_target <= 30:
                    #     # If the asteroid is within 10 pixels of the last target
                    #     continue
                if asteroid.velocity_direction is None or asteroid.velocity_magnitude is None:
                    # Skip asteroids that can't have movement tracked
                    continue
                a_diff = find_degree_of_movement(asteroid.x_center, asteroid.y_center, ship.x_center, ship.y_center)
                if a_diff < angle_diff:
                    # Set the distance to beat
                    angle_diff = a_diff
                    closest_asteroid = asteroid
            self.target = closest_asteroid

        # If a target wasn't found do nothing
        if self.target is None:
            return AsteroidsActions.DO_NOTHING.value
        elif not self.target.transposed:
            distance_to_target = find_distance(ship.x_center, ship.y_center, self.target.x_center, self.target.y_center)
            frames_until_missile_intersection = distance_to_target / Missile.SPEED
            angle_of_ship_to_asteroid = \
                find_degree_of_movement(self.target.x_center, self.target.y_center, ship.x_center, ship.y_center)
            frames_until_ship_oriented = abs(angle_of_ship_to_asteroid - ship.direction_deg) / Ship.TURNING_SPEED

            frames_asteroid_moves_before_being_hit = frames_until_ship_oriented + frames_until_missile_intersection

            # Transpose the coordinates of the asteroid to see where it
            # will be in 'frames_asteroid_moves_before_being_hit' frames
            x, y = x_y_split_based_on_angle(self.target.velocity_direction)
            x, y = x * frames_asteroid_moves_before_being_hit, y * frames_asteroid_moves_before_being_hit
            # Save the non-transposed target as the last target
            self.last_target = self.target
            self.target = transposed_asteroid = \
                Asteroid(matrix_add_vector(self.target.xy_positions, [[x], [y]]), self.board, transposed=True)
            self.target_angle = find_degree_of_movement(transposed_asteroid.x_center, transposed_asteroid.y_center,
                                                        ship.x_center, ship.y_center)

        angle_diff = self.target_angle - ship.direction_deg
        if abs(angle_diff) <= self.angle_tolerance:
            # The ship is in position to fire at the target
            self.target = None
            self.target_angle = None
            self.currently_shooting = True
            return AsteroidsActions.FIRE.value
        elif angle_diff > 0:
            # Turn left
            return AsteroidsActions.TURN_LEFT.value
        elif angle_diff < 0:
            # Turn right
            return AsteroidsActions.TURN_RIGHT.value
