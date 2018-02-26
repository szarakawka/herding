from ..herding import Herding


class Agent:

    def __init__(self, env: Herding):
        self.x = 0
        self.y = 0
        self.passive_agents = None
        self.active_agents = None

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def setLists(self, sheepList, dogList):
        self.dogList = dogList
        self.sheepList = sheepList


class PassiveAgent(Agent):

    def move(self):
        raise NotImplementedError


class ActiveAgent(Agent):

    def move(self, action):
        raise NotImplementedError
