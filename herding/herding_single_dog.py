from herding.assets.constants import EnvParams
from herding.assets.herding import Herding


class HerdingSingleDog(Herding):

        def __init__(self):
            params = EnvParams()
            params.DOG_COUNT = 1
            super().__init__(params)
