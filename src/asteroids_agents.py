import argparse
import random

import gym
from gym import logger

from agents.direction_minimize_agent import DegreeMinimizing
from agents.random_agent import RandomAgent
from agents.distance_minimize_agent import DistanceMinimizing

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
parser.add_argument('agent', metavar='agent', type=str, choices=['random', 'dis-min', 'deg-min'],
                    help='Specify the agent you want to use to play Asteroids.... '
                         'Available Agents: random, dis-min, deg-min')
parser.add_argument('--runs', dest='runs', metavar='N', type=int, nargs=1, default=1,
                    help='Number of games to play (default: 1)')
parser.add_argument('--seed', dest='seed', metavar='S', type=int, nargs=1, default=random.randint(1, 1000000),
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
    elif agent_arg == 'dis-min':
        agent = DistanceMinimizing(env.action_space)
    elif agent_arg == 'deg-min':
        agent = DegreeMinimizing(env.action_space)
    seed = asteroids_args.seed if isinstance(asteroids_args.seed, int) else asteroids_args.seed[0]
    runs = asteroids_args.runs if isinstance(asteroids_args.runs, int) else asteroids_args.runs[0]
    env.seed(seed)
    total_runs = 0
    total_score = 0
    while total_runs < runs:

        reward = 0
        done = False
        score = 0
        special_data = {'ale.lives': 3}
        ob = env.reset()
        i = 0
        while not done:
            action = agent.act(ob, reward, done)
            ob, reward, done, x = env.step(action)
            score += reward
            # env.render()
            i += 1
        print(f'Asteroids score [{i}]: {score}')
        total_runs += 1
        total_score += score

    print(f'Average score across {total_runs} runs: {total_score / total_runs}')

    # Close the env and write monitor result info to disk
    env.close()
