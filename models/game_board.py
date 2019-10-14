

class GameBoard:
    SHIP_RGB = [240, 128, 128]
    SCORE_RGB = [184, 50, 50]
    BLANK_RGB = [0, 0, 0]
    BLUE_MISSILE_RGB = [117, 181, 239]
    RED_MISSILE_RGB = [240, 128, 128]
    MISSILE_RGBS = [BLUE_MISSILE_RGB, RED_MISSILE_RGB]

    # Record all Entities created for each frame of the game, this can
    # be used to check previous frames to see Ship or Asteroid data
    GAME_OBJECTS = {}

    def __init__(self, game_map, frame: int):
        import models.entity as en
        self.game_map = game_map
        self.frame = frame

        # 210x160 array of initially False values
        self.explored_mapping = [[False for i in range(160)] for j in range(210)]

        GameBoard.GAME_OBJECTS[frame] = []
        self.ship: en.Ship = None
        self.asteroids: [en.Asteroid] = []

    def is_location_explored(self, x: int, y: int):
        return self.explored_mapping[x][y]

    def explore_location(self, x: int, y: int):
        self.explored_mapping[x][y] = True

    def check_pixel(self, x, y, RGB_VALS) -> bool:
        """
        Compare a pixel at a given x,y coord value with a given set of RGB values
        :return True if the pixel at x,y is the same as the RGB values supplied, False otherwise
        """
        return self.game_map[x][y][0] == RGB_VALS[0] and \
               self.game_map[x][y][1] == RGB_VALS[1] and \
               self.game_map[x][y][2] == RGB_VALS[2]

    def is_pixel_missile(self, x: int, y: int) -> bool:
        """
        Determines if the given location is an asteroid
        """
        for rgb_vals in GameBoard.MISSILE_RGBS:
            if self.check_pixel(x, y, rgb_vals):
                return True
        return False

    def register_entity(self, entity):
        """
        Add Entity to the mapping for this frame
        """
        import models.entity as en
        current_entity_array = GameBoard.GAME_OBJECTS[self.frame]
        current_entity_array.append(entity)
        GameBoard.GAME_OBJECTS[self.frame] = current_entity_array
        if isinstance(entity, en.Ship):
            self.ship = entity
        elif isinstance(entity, en.Asteroid):
            self.asteroids.append(entity)

    def get_last_ship(self):
        """
        :return: None if no Ships have appeared yet,
        otherwise the State of the ship in the most recent frame
        """
        import models.entity as en

        # Start from the last frame so we don't recall entities that are in the current frame
        i = self.frame - 1
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
        # Start from the last frame so we don't recall entities that are in the current frame
        i = self.frame - 1
        while i >= 0:
            for entity in GameBoard.GAME_OBJECTS[i]:
                if isinstance(entity, en.Asteroid):
                    asteroids.append(entity)
            if len(asteroids) > 0:
                return asteroids
            i -= 1
        return []

    def get_last_missile(self, missile_type: int):
        """
        Get the last red or blue missile (depending on the type specified)
        """
        import models.entity as en

        # Start from the last frame so we don't recall entities that are in the current frame
        i = self.frame - 1
        # Don't go past two additional frames, missiles beyond that point are probably not the same
        j = self.frame - 3
        while i >= 0 and i >= j:
            for entity in GameBoard.GAME_OBJECTS[i]:
                if isinstance(entity, en.Missile):
                    if entity.missile_type == missile_type:
                        return entity
            i -= 1
        return None

    def gather_connecting_pixels(self, x: int, y: int):
        """
        Get all pixels that are connected and are the same color as the provided x,y pixel
        :return: List of x,y coordinate pairs
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
                        if not (x_cur < 0 or y_cur < 0) \
                                and not (x_cur >= 210 or y_cur >= 160) \
                                and not self.is_location_explored(x_cur, y_cur) \
                                and [x_cur, y_cur] not in pixel_locations \
                                and [x_cur, y_cur] not in new_pixels \
                                and self.check_pixel(x_cur, y_cur, self.game_map[x][y]):
                            # Only look at the position if it the x, y coords are greater than 0
                            # and the x,y coords are less than the bounds of the game board
                            # and hasn't been explored yet
                            # and it isn't already in our pixel location set
                            # and it isn't already in our new pixel array
                            # and the position has the same RBG values as the original location given
                            new_pixels.append([x_cur, y_cur])
                            self.explore_location(x_cur, y_cur)
                    j += 1
                i += 1
                j = -1
        return pixel_locations
