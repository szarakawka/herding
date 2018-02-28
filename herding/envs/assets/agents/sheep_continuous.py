from .agent import PassiveAgent
from ..herding import Herding

class SheepContinuous(PassiveAgent):

    def __init__(self, env: Herding):
        super().__init__(env)

    def move(self):
        pass
