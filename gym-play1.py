import argparse
import sys
import pdb
import time

import gym
from gym import wrappers, logger

from models import Ship, GameBoard
from util import print_board




class Agent(object):
    last_action = 0
    last_ship = None

    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    # You should modify this function
    def act(self, observation, reward, done):
        zero_count = non_zero_count = 0
        asteroids = None
        board = GameBoard(observation)

        rgb_colors = set()
        ship_pixels = []

        x, y = 0, 0

        print_board(board)

        while x < len(observation):
            while y < len(observation[0]):
                rgb_vals = observation[x][y]
                if board.check_pixel(x, y, GameBoard.BLANK_RGB):
                    zero_count += 1
                elif board.check_pixel(x, y, GameBoard.SHIP_RGB):
                    ship_pixels.append([x, y])
                else:
                    # print(f'POS: {x}, {y}')
                    rgb_string = f'{rgb_vals[0]}, {rgb_vals[1]}, {rgb_vals[2]}'
                    # print(f'RGB: {rgb_string}')
                    non_zero_count += 1
                    rgb_colors.add(rgb_string)
                y += 1
            x += 1
            y = 0

        for rgb in rgb_colors:
            print(f'RGB Color: {rgb}')
        if len(ship_pixels) is not 0:
            self.last_ship = Ship(ship_pixels, self.last_ship)

        print(f'Zero: {zero_count}, Non Zero: {non_zero_count}')
        return 3
        # if self.last_action is 5:
        #     self.last_action = 4
        #     return 4
        # else:
        #     self.last_action = 5
        #     return 5





# YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
# ANOTHER MAIN PROGRAM
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='Asteroids-v0', help='Select the environment to run')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = gym.make(args.env_id)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = 'random-agent-results'


    env.seed(0)
    agent = Agent(env.action_space)

    episode_count = 100
    reward = 0
    done = False
    score = 0
    special_data = {}
    special_data['ale.lives'] = 3
    ob = env.reset()
    i = 0
    while not done:
        i += 1
        action = agent.act(ob, reward, done)
        ob, reward, done, x = env.step(action)
        # pdb.set_trace()
        score += reward
        env.render()
        time.sleep(20/1000)

    # Close the env and write monitor result info to disk
    print ("Your score: %d" % score)
    env.close()
