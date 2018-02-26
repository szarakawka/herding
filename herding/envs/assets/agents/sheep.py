from .agent import Agent


class Sheep(Agent):

    def __init__(self, envParams: EnvParams):
        super().__init__(envParams)


    def move(self):
        deltaX = 0
        deltaY = 0
        for dog in self.dogList:
            distance = pow(pow((self.x - dog.x), 2) + pow((self.y - dog.y), 2), 0.5)
            if distance < 100:
                if distance < 50:
                    distance = 50
                deltaX += ((self.x - dog.x) / distance) * (100 - distance)
                deltaY += ((self.y - dog.y) / distance) * (100 - distance)

        if deltaX > 50 or deltaY > 50:
            if deltaX > deltaY:
                deltaY = deltaY / deltaX * 50
                deltaX = 50
            else:
                deltaX = deltaX / deltaY * 50
                deltaY = 50

        deltaX = deltaX / 50 * self.params.MAX_MOVEMENT_DELTA
        deltaY = deltaY / 50 * self.params.MAX_MOVEMENT_DELTA
        self.x += deltaX
        self.y += deltaY


    def _complexMove(self):
        # TODO
        pass