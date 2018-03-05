import math
import numpy as np
from .agent import ActiveAgent
from .. import constants
DEG2RAD = 0.01745329252


class Dog(ActiveAgent):

    RAYS = 0
    TARGETS = 1
    LENGTH_TO_CENTER = 0
    TAN_TO_CENTER = 1

    
    def __init__(self, env):
        super().__init__(env)
        
        self.rotation_mode = env.rotation_mode
        self.ray_count = env.ray_count
        self.ray_length = env.ray_length
        self.max_movement_speed = env.max_movement_speed
        self.max_rotation_speed = env.max_rotation_speed
        self.field_of_view = env.field_of_view
        self.herd_centre_point = env.herd_centre_point
        
        self.rotation = 0
        self.rayRadian = []
        
        for i in range(self.ray_count):
            self.rayRadian.append((math.pi + ((180 - self.field_of_view) / 360) * math.pi + (self.field_of_view / (self.ray_count - 1)) * DEG2RAD * i) % 2 * math.pi)
        if self.rayRadian[0] > self.rayRadian[self.ray_count - 1]:
            self.wideView = True
        else:
            self.wideView = False

        for i, _ in enumerate(self.observation[self.RAYS]):
            self.observation[self.RAYS][i] = 0
            self.observation[self.TARGETS][i] = 0

    def move(self, action):
        deltaX = action[0] * self.max_movement_speed
        deltaY = action[1] * self.max_movement_speed

        vecLength = math.sqrt(deltaX*deltaX + deltaY * deltaY)
        if vecLength > self.max_movement_speed:
            norm = self.max_movement_speed / vecLength
            deltaX *= norm
            deltaY *= norm

        """
        Rotacja jest w radianach (0, 2 * math.pi), action[2] jest od (-1, 1),
        MAX_ROTATION_DELTA (0, 360)
        """
        if self.rotation_mode is constants.RotationMode.FREE:
            self.rotation += action[2] * self.max_rotation_speed * DEG2RAD
            self.rotation = self.rotation % 2 * math.pi
        else:
            self.rotation = np.arctan2(self.y - self.herd_centre_point[1], self.x - self.herd_centre_point[0]) + 90 * DEG2RAD

        cosRotation = math.cos(self.rotation)
        sinRotation = math.sin(self.rotation)
        self.x += deltaX * cosRotation + deltaY * sinRotation
        self.y += deltaY * -cosRotation + deltaX * sinRotation

    def clearObservation(self):
        for i, _ in enumerate(self.observation[self.RAYS]):
            self.observation[self.RAYS][i] = 0
            self.observation[self.TARGETS][i] = 0

    def getDistanceFromAgent(self, agent):
        return pow(pow((self.x - agent.x), 2) + pow((self.y - agent.y), 2), 0.5)

    def calculateAngle(self, agent):
        tempAngle = math.atan2(self.y - agent.y, self.x - agent.x) - self.rotation
        while tempAngle < 0:
            tempAngle += 2 * math.pi
        return tempAngle

    def calculateDelta(self, rayTan, agent):
        return pow((2 * (self.x - agent.x)) + (2 * rayTan * (self.y - agent.y)), 2) - (4 * (1 + pow(rayTan, 2)) * (-1 * pow(self.radius, 2) + pow(self.x - agent.x, 2) + pow(self.y - agent.y, 2)))

    def calculateStraightToCircleDistance(self, agent, index):
        return abs(-1 * math.tan(self.rotation - self.rayRadian[index]) * (self.x - agent.x) + self.y - agent.y) / pow(pow(math.tan(self.rotation - self.rayRadian[index]), 2) + 1, 0.5)

    def isInSight(self, tempAngle):
        if self.wideView:
            if not self.rayRadian[self.ray_count-1] < tempAngle < self.rayRadian[0]:
                return True
        else:
            if self.rayRadian[0] < tempAngle < self.rayRadian[self.ray_count-1]:
                return True
        return False

    def setDistanceAndColor(self, index, agent):
        rayTan = math.tan(self.rotation - self.rayRadian[index])
        delta = self.calculateDelta(rayTan, agent)
        x1 = (((2 * (self.x - agent.x)) + (2 * rayTan * (self.y - agent.y))) - math.pow(delta, 0.5)) / (2 * (1 + pow(rayTan, 2)))
        y1 = rayTan * x1
        x2 = (((2 * (self.x - agent.x)) + (2 * rayTan * (self.y - agent.y))) + math.pow(delta, 0.5)) / (2 * (1 + pow(rayTan, 2)))
        y2 = rayTan * x2
        distance1 = pow(pow(x1, 2) + pow(y1, 2), 0.5)
        distance2 = pow(pow(x2, 2) + pow(y2, 2), 0.5)
        if distance1 < distance2:
            distance = distance1 - self.radius
        else:
            distance = distance2 - self.radius
        if 1 - (distance / self.ray_length) > self.observation[self.RAYS][index]:
            self.observation[self.RAYS][index] = 1 - (distance / self.ray_length)
            self.observation[self.TARGETS][index] = 1 if type(agent) is Dog else -1

    def iterateRays(self, distance, agent, index, iterator):
        while 0 <= index <= self.ray_count - 1:
            circleDistance = self.calculateStraightToCircleDistance(agent, index)
            if circleDistance <= self.radius:
                if (distance - (2 * self.radius)) / self.ray_length < 1 - self.observation[self.RAYS][index]:
                    self.setDistanceAndColor(index, agent)
            else:
                break
            index += iterator

    def colorRays(self, tempAngle, distance, agent):
        if tempAngle < self.rayRadian[0]:
            tempAngle += 2 * math.pi
        left = self.ray_count - 2 - int((tempAngle - self.rayRadian[0]) / ((self.field_of_view / (self.ray_count - 1)) * DEG2RAD))
        right = left + 1
        # color left rays
        self.iterateRays(distance, agent, left, -1)
        # color right rays
        self.iterateRays(distance, agent, right, 1)

    def updateObservationToCenter(self):
        lastIndex = self.ray_count
        absX = abs(self.x - self.herd_centre_point[0])
        absY = abs(self.y - self.herd_centre_point[1])
        self.observation[self.LENGTH_TO_CENTER][lastIndex] = pow(pow(absX, 2) + pow(absY, 2), 0.5) / self.ray_length
        self.observation[self.TAN_TO_CENTER][lastIndex] = (((np.arctan2(absX, absY) + self.rotation) % 2 * math.pi) * 2) / 2 * math.pi - 1

    def updateObservation(self):
        """
        Metoda przeprowadzająca raytracing. Zmienna observation wskazuje na tablicę observation_space[i]
        środowiska, gdzie indeks 'i' oznacza danego psa.
        """
        self.clearObservation()
        for agent in self.sheep_list + self.dog_list:
            distance = self.getDistanceFromAgent(agent)
            if distance - (2 * self.radius) < self.ray_length:
                tempAngle = self.calculateAngle(agent)
                if self.isInSight(tempAngle):
                    self.colorRays(tempAngle, distance, agent)
        self.updateObservationToCenter()

class RayTracing:
    pass