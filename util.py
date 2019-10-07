import math

from models.game_board import GameBoard


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
