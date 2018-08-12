from gym.envs.registration import register

register(
    id='hearts-v0',
    entry_point='gymhearts.env::HeartsEnv'
)
