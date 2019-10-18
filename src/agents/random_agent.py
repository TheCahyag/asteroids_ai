from agents.abstract_agent import AbstractAgent


class RandomAgent(AbstractAgent):
    """
    Random Agent that chooses its actions in a random manner
    """

    def act(self, observation, reward: int, done: bool) -> int:
        return self.action_space.sample()
