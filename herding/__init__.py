#tutaj konfiguracje
from gym.envs.registration import register

# register(
#     id='herding-v0',
#     entry_point='gym_soccer.envs:HerdingEnv',
#     timestep_limit=1000,
#     reward_threshold=1.0,
#     nondeterministic = True,
# )

register(
    id='single-dog-v0',
    entry_point='herding:HerdingSingleDog',
)