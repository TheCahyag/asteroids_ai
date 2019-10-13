import argparse
import random
import time

import gym
from gym import logger

from agents.random_agent import RandomAgent
from agents.shooting_agent import ShootingAgent

# Structuring the arguments
parser = argparse.ArgumentParser(description='Main program to run Asteroids using an agent to play. This easily '
                                             'allows switching agents and gives the ability to execute multiple '
                                             'Asteroids runs.\n\n'
                                             'Example: asteroids_agents.py random --runs 5\n\t'
                                             ' Run the random agent for 5 games\n'
                                             'Example: asteroids_agents.py shooting\n\t'
                                             ' Run the shooting agent for a single game',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog='Programmed by Brandon Bires-Navel (brn5915@rit.edu)')
parser.add_argument('agent', metavar='agent', type=str, choices=['random', 'shooting'],
                    help='Specify the agent you want to use to play Asteroids.... Available Agents: Random, Shooting')
parser.add_argument('--runs', dest='runs', metavar='N', type=int, nargs=1, default=1,
                    help='Number of games to play (default: 1)')
parser.add_argument('--seed', dest='seed', metavar='S', type=int, nargs=1, default=random.randint,
                    help='Seed to set for the environment (default: random integer)')

if __name__ == '__main__':
    logger.set_level(logger.INFO)
    env = gym.make('AsteroidsNoFrameskip-v4')

    # Select which agent to use based on the command line arguments
    agent = None
    asteroids_args = parser.parse_args()

    agent_arg = asteroids_args.agent
    if agent_arg == 'random':
        agent = RandomAgent(env.action_space)
    elif agent_arg == 'shooting':
        agent = ShootingAgent(env.action_space)

    env.seed(asteroids_args.seed[0])
    runs = 0
    while runs < asteroids_args.runs[0]:

        reward = 0
        done = False
        score = 0
        special_data = {'ale.lives': 3}
        ob = env.reset()
        i = 0
        while not done:
            i += 1
            action = agent.act(ob, reward, done)
            ob, reward, done, x = env.step(action)
            score += reward
            env.render()
            # time.sleep(20 / 1000)
        print(f'Asteroids score [{i}]: {score}')
        runs += 1

    # Close the env and write monitor result info to disk
    env.close()
