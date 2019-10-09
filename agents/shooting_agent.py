from agents.abstract_agent import AbstractAgent
from models.actions import AsteroidsActions


class ShootingAgent(AbstractAgent):

    def __init__(self, action_space):
        super().__init__(action_space)

    def act(self, observation, reward: int, done: bool) -> int:
        # This processes the data from the observation
        super().act(observation, reward, done)
        if done:
            return AsteroidsActions.DO_NOTHING.value
        self.frame += 1
        return AsteroidsActions.FIRE_TURN_RIGHT.value
