import copy
from typing import List
from ..herding import Herding

class Agent:

    def __init__(self, env: Herding):
        self.x = 0
        self.y = 0
        self.radius = env.agent_radius
        self.dog_list: List[ActiveAgent] = copy.copy(env.dog_list).remove(self)
        self.sheep_list: List[PassiveAgent] = copy.copy(env.sheep_list).remove(self)

    def set_pos(self, x, y):
        self.x = x
        self.y = y


class PassiveAgent(Agent):

    def move(self):
        raise NotImplementedError


class ActiveAgent(Agent):

    def move(self, action):
        raise NotImplementedError

    def update_observation(self):
        raise NotImplementedError
