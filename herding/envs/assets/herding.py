import gym
import numpy as np
from gym import spaces
from typing import List
from .constants import *
from . import agents


class Herding(gym.Env):

    metadata = {
        'render.modes': ['human']
    }

    def __init__(
            self,
            dog_count=1,
            sheep_count=3,
            agent_layout=AgentsLayout.RANDOM,
            sheep_type=SheepType.SIMPLE,
            max_movement_speed=5,
            max_rotation_speed=90,
            continuous_sheep_spread_rate=1,
            ray_count=180,
            ray_length=600,
            rotation_mode=RotationMode.FREE,
    ):
        self.dog_count = dog_count
        self.sheep_count = sheep_count
        self.agent_layout = agent_layout
        self.sheep_type = sheep_type
        self.max_movement_speed = max_movement_speed
        self.max_rotation_speed = max_rotation_speed
        self.ray_count = ray_count
        self.ray_length = ray_length
        self.rotation_mode = rotation_mode

        self.map_height = 1280
        self.map_width = 1024
        self.agent_radius = 5

        self.dog_list, self.sheep_list = self._create_agents()
        self.state = self._create_state()
        self._viewer = None
        self.herd_centre_point = [0, 0]
        self.reward_counter = RewardCounter(self)

    def step(self, action):
        for i, dog in enumerate(self.dog_list):
            dog.move(action[i])

        for sheep in self.sheep_list:
            sheep.move()

        for dog in self.dog_list:
            dog.updateObservation()

        reward = self.reward_counter.get_reward()
        is_done = self.reward_counter.is_done()

        return self.state, reward, is_done, {}

    def reset(self):
        # Metoda statyczna klasy AgentsLayout. Wyjątkowo przyjmuje parametr self.
        self.setUpAgents(self)
        self.epoch = 0
        for dog in self.dogList:
            dog.updateObservation()

        return self.state

    def render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        if self.viewer is None:
            from herding.envs.assets.rendering import Renderer
            self.viewer = Renderer(self)

        self.viewer.render()

    def seed(self, seed=None):
        pass

    @property
    def action_space(self):
        dim = 3 if self.rotationMode is RotationMode.FREE else 2
        singleActionSpace = spaces.Box(-1, 1, (dim,))
        return spaces.Tuple((singleActionSpace,) * self.dogCount)

    @property
    def observation_space(self):
        singleObservationSpace = spaces.Box(-1, 1, (2, self.raysCount))
        return spaces.Tuple((singleObservationSpace,) * self.dogCount)

    def _create_agents(self):
        dog_list: List[agents.ActiveAgent] = []
        sheep_list: List[agents.PassiveAgent] = []
        Sheep = agents.get_sheep_class(self.sheep_type)

        for i in range(self.sheep_count):
            sheep_list.append(Sheep(self))
        for i in range(self.dog_count):
            dog_list.append(agents.Dog(self))

        return dog_list, sheep_list

        # TODO implement it in agents
        # for i in range(self.sheep_count):
        #     self.sheep_list[i].setLists(np.delete(self.sheep_list, i), list(np.array(self.dog_list)))
        #
        # for i in range(self.dog_count):
        #     self.dog_list[i].setLists(self.sheep_list, list(np.delete(self.dog_list, i)))

    def _create_state(self):
        return np.ndarray(shape=(self.dog_count, 2, self.ray_count + 1), dtype=float)

    def _calculate_herd_centre(self):
        pass

    def set_up_agents(self):
        pass
    # def _checkIfDone(self):
    #     if self.scatter < self.params.SCATTER_LEVEL:
    #         return True
    #
    #     return False
    #
    # def _scatter(self):
    #     self.herdCentrePoint[0] = self.herdCentrePoint[1] = 0
    #     for sheep in self.sheepList:
    #         self.herdCentrePoint[0] += sheep.x
    #         self.herdCentrePoint[1] += sheep.y
    #
    #     self.herdCentrePoint[0] /= self.sheepCount
    #     self.herdCentrePoint[1] /= self.sheepCount
    #
    #     self.previousScatter = self.scatter
    #     self.scatter = 0
    #     for sheep in self.sheepList:
    #         self.scatter += (sheep.x - self.herdCentrePoint[0]).__pow__(2) + (
    #             sheep.y - self.herdCentrePoint[1]).__pow__(2)
    #
    # def _reward(self):
    #     self._scatter()
    #     self.rewardValue = self.previousScatter - self.scatter
    #     if self.scatter < self.previousScatter:
    #         self.rewardValue.__neg__()
    #     if self.scatter < self.params.SCATTER_LEVEL:
    #         self.rewardValue = self.params.REWARD_FOR_HERDING
    #
    #     return self.rewardValue


class RewardCounter:

    def __init__(self, env: Herding):
        self.herd_centre_point = env
        self.sheep_type = env.sheep_type
        self.previous_scatter = 0
        self.scatter = 0
        self.reward_value = 0
        self.constants_scatter_counter = 0

    def is_done(self):
        return False

    def get_reward(self):
        return 0

    def _scatter(self):
        return 0


class AgentsLayoutFunction:

    @staticmethod
    def random(self: Herding):
        padding = 5
        for agent in self.dog_list + self.sheep_list:
            x = random.randint(agent.radius + padding, self.map_width - agent.radius - padding)
            y = random.randint(agent.radius + padding, self.map_height - agent.radius - padding)
            agent.set_pos(x, y)

    @staticmethod
    def layout1(self: Herding):
        padding = 5
        for agent in self.dog_list:
            x = random.randint(agent.radius + padding, self.map_width - agent.radius - padding)
            y = random.randint(agent.radius + padding, self.map_height - agent.radius - padding)
            agent.set_pos(x, y)

        w_padding = int(self.map_width / 6)
        h_padding = int(self.map_height / 6)
        for agent in self.sheep_list:
            x = random.randint(agent.radius + w_padding, self.map_width - agent.radius - w_padding)
            y = random.randint(agent.radius + h_padding, self.map_height - agent.radius - h_padding)
            agent.set_pos(x, y)

    @staticmethod
    def layout2(self: Herding):
        # TODO
        pass
