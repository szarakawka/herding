from gym.envs.registration import register

register(
    id='herding-singleDog-v0',
    entry_point='herding.envs:HerdingSingleDog',
    timestep_limit=1000,
    nondeterministic=False,
)
