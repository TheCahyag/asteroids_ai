

class GameBoard:
    SHIP_RGB = [240, 128, 128]
    SCORE_RGB = [184, 50, 50]
    BLANK_RGB = [0, 0, 0]
    ASTEROID_RGBS = [
        [214, 214, 214],
        [180, 122, 48],
        [187, 187, 53]
    ]
    MISSILE_RGB = [117, 181, 239]

    # Record all Entities created for each frame of the game, this can
    # be used to check previous frames to see Ship or Asteroid data
    GAME_OBJECTS = {}

    def __init__(self, game_map, frame: int):
        self.game_map = game_map
        self.frame = frame

        # 210x160
        self.explored_mapping = [[False for i in range(160)] for j in range(210)]

        GameBoard.GAME_OBJECTS[frame] = []

    def is_location_explored(self, x: int, y: int):
        return self.explored_mapping[x][y]

    def explore_location(self, x: int, y: int):
        self.explored_mapping[x][y] = True

    def check_pixel(self, x, y, RGB_VALS):
        """
        Compare a pixel at a given x,y coord value with a given set of RGB values
        :return True if the pixel at x,y is the same as the RGB values supplied, False otherwise
        """
        return self.game_map[x][y][0] == RGB_VALS[0] and \
               self.game_map[x][y][1] == RGB_VALS[1] and \
               self.game_map[x][y][2] == RGB_VALS[2]

    def is_pixel_asteroid(self, x: int, y: int):
        """
        Determines if the given location is an asteroid
        """
        for rgb_vals in GameBoard.ASTEROID_RGBS:
            if self.check_pixel(x, y, rgb_vals):
                return True
        return False

    def register_entity(self, entity):
        """
        Add Entity to the mapping for this frame
        """
        current_entity_array = GameBoard.GAME_OBJECTS[self.frame]
        current_entity_array.append(entity)
        GameBoard.GAME_OBJECTS[self.frame] = current_entity_array

    def get_last_ship(self):
        """
        :return: None if no Ships have appeared yet,
        otherwise the State of the ship in the most recent frame
        """
        import models.entity as en

        i = self.frame
        while i >= 0:
            for entity in GameBoard.GAME_OBJECTS[i]:
                if isinstance(entity, en.Ship):
                    return entity
            i -= 1
        return None

    def get_last_asteroids(self):
        """
        :return: Get the list of Asteroids from the most recent
        frame that had asteroids, otherwise an empty list
        """
        import models.entity as en

        asteroids: [en.Asteroid] = []
        i = self.frame
        while i >= 0:
            for entity in GameBoard.GAME_OBJECTS[i]:
                if isinstance(entity, en.Asteroid):
                    asteroids.append(entity)
            if len(asteroids) > 0:
                return asteroids
            i -= 1
        return []

    def get_last_missile(self):
        import models.entity as en

        i = self.frame
        while i >= 0:
            for entity in GameBoard.GAME_OBJECTS[i]:
                if isinstance(entity, en.Missile):
                    return entity
            i -= 1
        return None
