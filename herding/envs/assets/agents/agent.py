from ..herding import Herding

class Agent:

    def __init__(self, env: Herding):
        self.x = 0
        self.y = 0
        self.radius = env.agent_radius
        self.dog_list = env.dog_list
        self.sheep_list = env.sheep_list

    def set_pos(self, x, y):
        self.x = x
        self.y = y


class PassiveAgent(Agent):

    def move(self):
        raise NotImplementedError


class ActiveAgent(Agent):

    def move(self, action):
        raise NotImplementedError
