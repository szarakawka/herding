#OpenAI Gym herding environment

Installation
============
1. Download the package and unzip it.
2. Execute "pip install -e <package directory>

Usage
============

    import gym
    env = gym.make('herding-singleDog-v0')
    env.reset()
    env.render()