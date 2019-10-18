from models.game_board import GameBoard

debug = False
p_board = False


def print_me(obj):
    import models.entity as en

    if debug and (isinstance(obj, en.Ship) or isinstance(obj, en.Missile)):
        print(obj)


def print_asteroid(asteroid):
    import models.entity as en
    asteroid: en.Asteroid = asteroid
    x_low, x_high = asteroid.x_low, asteroid.x_high
    y_low, y_high = asteroid.y_low, asteroid.y_high
    x = x_low
    y = y_low
    string = ''
    while x <= x_high:
        while y <= y_high:
            if [x, y] in asteroid.xy_positions:
                string = string + 'X'
            else:
                string = string + '.'
            y += 1
        string = string + '\n'
        x += 1
        y = y_low
    print(string)


def print_board(board: GameBoard):
    if debug and p_board:
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
