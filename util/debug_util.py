def print_asteroid(asteroid):
    import models.entity as en
    asteroid: en.Asteroid = asteroid
    x_low, x_high = asteroid.x_low, asteroid.x_high
    y_low, y_high = asteroid.y_low, asteroid.y_high


def print_board(board: GameBoard):
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