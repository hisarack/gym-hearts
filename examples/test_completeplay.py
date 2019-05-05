import gym
from gymhearts import env as hearts_env

from treys import Card

from utils import logger
from strategy.firstplay import FirstPlayStrategy
from strategy.lowplay import LowPlayStrategy
from strategy.completeplay import CompletePlayStrategy


env = hearts_env.HeartsEnv()
env.add_player(CompletePlayStrategy())
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
    # if len(observation['playing_ids']) == 4:
    #    env.render()
