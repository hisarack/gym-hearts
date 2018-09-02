# Gym Hearts

This is an experimental library for hearts poker game and reinforment learning.
I implement the library and run it at ubuntu and mac by python3.
If you encounter any problem, feel free to create new issue on this project :smile:


# Implemented Rules

1. All heart cards ( 2♥, 3♥, …., Q♥, K♥, A♥ ) cost 1 score
2. Q♠ costs 13 score
3. This trick’s looser will be next trick’s first player
4. Shooting the moon

# Installation

```sh
pip3 install gym-hearts
```

# Hello World

```python
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
```

# Observation

```json
{
  "trick": 12, 
  "round": 9, 
  "number_of_players": 4, 
  "scores": [50, 104, 40, 40], 
  "playing_cards": [69634, 2102541, 541447], 
  "playing_ids": [3, 0, 1], 
  "hand_cards": [529159], 
  "current_player_id": 2, 
  "valid_hand_cards": [529159], 
  "number_of_hand_cards_for_all_players": [0, 0, 1, 0]
 }
```

# Render

```sh
--------GAME-------
round: 9
trick: 11
-------PLAYER------
player 0
[7♠]
score: 50
player 1
[5♦]
score: 104
player 2
[5♠] [T♠]
score: 40
player 3
[2♠]
score: 40
--------BOARD-------
[9♠] [3♦] [] [8♦]
--------------------
```
