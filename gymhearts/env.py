import gym

from treys.card import Card
from treys.deck import Deck

from .player import Player
from .evaluator import Evaluator


class HeartsEnv(gym.Env):

    def __init__(self):
        self._number_of_players = 4
        self._evaluator = Evaluator()
        self._deck = Deck()
        self._deck.shuffle()
        self._players = [Player(i, self._deck.draw(13)) for i in range(self._number_of_players)]
        self._trick = 0
        self._playing_cards = []
        self._playing_ids = []
        self._current_player_id = 0

    def get_observation(self):
        return {
            'hand_cards': self._players[self._current_player_id].get_hand_cards(),
            'score': self._players[self._current_player_id].get_score(),
            'playing_cards': self._playing_cards.copy(),
            'playing_ids': self._playing_ids.copy()
        }

    def step(self, action_card):
        if len(self._playing_cards) == self._number_of_players:
            self._playing_cards.clear()
            self._playing_ids.clear()
        self._players[self._current_player_id].remove_hand_card(action_card)
        self._playing_cards.append(action_card)
        self._playing_ids.append(self._current_player_id)
        if len(self._playing_cards) == self._number_of_players:
            self._trick += 1
            punish_score, punish_player_id = self._evaluator.evaluate(self._playing_cards, self._playing_ids)
            self._players[punish_player_id].add_score(punish_score)
        done = self._trick == 13
        rewards = [0] * self._number_of_players
        info = {}
        if len(self._playing_cards) == self._number_of_players:
            self._current_player_id = punish_player_id
            rewards[punish_player_id] = punish_score
        else:
            self._current_player_id += 1
            self._current_player_id = self._current_player_id % 4
        observation = self.get_observation()
        return observation, rewards, done, info

    def reset(self):
        self._deck = Deck()
        self._deck.shuffle()
        self._players = [Player(i, self._deck.draw(13)) for i in range(self._number_of_players)]
        self._trick = 0
        self._playing_cards = []
        self._playing_ids = []
        self._current_player_id = 0

    def render(self, mode='human', close=False):
        print("-------PLAYER------")
        for i in range(self._number_of_players):
            print("player {}".format(i))
            Card.print_pretty_cards(self._players[i].get_hand_cards())
            print("score: {}".format(self._players[i].get_score()))
        print("--------BOARD-------")
        Card.print_pretty_cards(self._playing_cards)
        print("--------------------")
