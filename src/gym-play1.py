import argparse

import gym
from gym import logger

from agents.random_agent import RandomAgent
from agents.distance_minimize_agent import DistanceMinimizing
from agents.direction_minimize_agent import DegreeMinimizing


# class Agent(RandomAgent):
class Agent(DistanceMinimizing):
# class Agent(DegreeMinimizing):

    def __init__(self, action_space):
        super().__init__(action_space)

    def act(self, observation, reward, done):
        return super().act(observation, reward, done)


## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
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
    while not done:
        action = agent.act(ob, reward, done)
        ob, reward, done, x = env.step(action)
        # pdb.set_trace()
        # sleep(30)
        score += reward
        env.render()

    # Close the env and write monitor result info to disk
    print("Your score: %d" % score)
    env.close()
