from herding.envs.assets.herding import Herding
from herding.envs.assets.constants import EnvParams

class HerdingSingleDog(Herding):


        def __init__(self):
            params = EnvParams()
            params.DOG_COUNT = 1
            super().__init__(params)
