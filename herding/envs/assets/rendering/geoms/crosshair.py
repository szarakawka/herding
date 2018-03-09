from .geom import *
from gym.envs.classic_control import rendering


class Crosshair(Geom):

    def __init__(self, env):
        self.herdCentrePoint = env.herd_centre_point
        crosshairSize = 10
        color = (0, 0, 0)
        self.verticalBar = Part(rendering.Line((-crosshairSize - 1, 0), (crosshairSize, 0)))
        self.horizontalBar = Part(rendering.Line((0, -crosshairSize - 1), (0, crosshairSize)))
        self.herd_circle = Part(rendering.make_circle(env.herd_target_radius, res=50, filled=False))

        self.verticalBar.setColor(*color)
        self.horizontalBar.setColor(*color)
        self.herd_circle.setColor(*color)

    def getParts(self):
        return [self.verticalBar.body, self.horizontalBar.body, self.herd_circle.body]

    def update(self):
        self.horizontalBar.setPos(self.herdCentrePoint[0], self.herdCentrePoint[1])
        self.verticalBar.setPos(self.herdCentrePoint[0], self.herdCentrePoint[1])
        self.herd_circle.setPos(self.herdCentrePoint[0], self.herdCentrePoint[1])
