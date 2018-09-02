import gym
from gymhearts import env as hearts_env
from gymhearts import strategy


class HelloStrategy(strategy.IStrategy):

    def move(self, observation):
        action = observation['valid_hand_cards'][0]
        return action


env = hearts_env.HeartsEnv()
env.enable_shooting_the_moon()
env.add_player(HelloStrategy())
env.add_player(HelloStrategy())
env.add_player(HelloStrategy())
env.add_player(HelloStrategy())
env.start()
env.render()
observation = env.get_observation()
done = False
while not done:
    action = env.move()
    observation, reward, done, info = env.step(action)
    env.render()
