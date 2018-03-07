from .agent import PassiveAgent


class SheepSimple(PassiveAgent):

    def __init__(self, env):
        super().__init__(env)

        self.max_movement_speed = env.max_movement_speed

    def move(self):
        deltaX = 0
        deltaY = 0
        for dog in self.dog_list:
            distance = pow(pow((self.x - dog.x), 2) + pow((self.y - dog.y), 2), 0.5)
            if distance < 200:
                if distance < 50:
                    distance = 50
                deltaX += ((self.x - dog.x) / distance) * (200 - distance)
                deltaY += ((self.y - dog.y) / distance) * (200 - distance)

        if deltaX > 50 or deltaY > 50:
            if deltaX > deltaY:
                deltaY = deltaY / deltaX * 50
                deltaX = 50
            else:
                deltaX = deltaX / deltaY * 50
                deltaY = 50

        deltaX = deltaX / 50 * self.max_movement_speed
        deltaY = deltaY / 50 * self.max_movement_speed
        self.x += deltaX
        self.y += deltaY
