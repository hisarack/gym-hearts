import gym
from gymhearts import env as hearts_env
from gymhearts import strategy

from utils import logger

from strategy.firstplay import FirstPlayStrategy


env = hearts_env.HeartsEnv()
env.add_player(FirstPlayStrategy())
env.add_player(FirstPlayStrategy())
env.add_player(FirstPlayStrategy())
env.add_player(FirstPlayStrategy())
env.start()
# env.render()
observation = env.get_observation()
print("{}: {}".format(observation['round'], observation['scores']))
done = False
while not done:
    action = env.move()
    observation, reward, done, info = env.step(action)
    if (observation['trick'] == 0 and len(observation['playing_ids']) == 0) or (done is True):
        print("{}: {}".format(observation['round'], observation['scores']))
    # env.render()
