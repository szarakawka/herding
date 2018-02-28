import math
import random

PI = math.pi
TWOPI = 2 * PI
DEG2RAD = 0.01745329252
EULER = math.e


class SheepType:
    SIMPLE, COMPLEX, CONTINUOUS = range(3)


class RotationMode:
    FREE, LOCKED_ON_HERD_CENTRE = range(2)


class AgentsLayout:
    RANDOM, LAYOUT1, LAYOUT2 = range(3)


# class EnvParams:
#
#     def __init__(self):
#         self.SHEEP_COUNT = 7
#         self.DOG_COUNT = 2
#         self.AGENT_RADIUS = 15
#         self.SHEEP_BEHAVIOUR = SheepBehaviour.SIMPLE
#         self.FIELD_OF_VIEW = 180
#         self.RAYS_COUNT = 128
#         self.RAY_LENGTH = 300
#         self.MAX_MOVEMENT_DELTA = 5
#         self.MAX_ROTATION_DELTA = 90
#         self.MAP_HEIGHT = 800
#         self.MAP_WIDTH = 1200
#         self.LAYOUT_FUNCTION = AgentsLayout.RANDOM
#         self.ROTATION_MODE = RotationMode.FREE
#         self.REWARD_FOR_HERDING = 10
#         self.REWARD = 0.2
#         self.EPOCH = 1000
#         self.SCATTER_LEVEL = 200
