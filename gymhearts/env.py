import gym

from treys.card import Card
from treys.deck import Deck

from .player import Player
from .evaluator import Evaluator


class HeartsEnv(gym.Env):

    def __init__(self, endgame_score=100):
        self._evaluator = Evaluator()
        self._number_of_players = 0
        self._number_of_hand_card_per_player = 0
        self._players = []
        self._trick = 0
        self._round = 0 # each round has 13 trick when we have 4 players
        self._playing_cards = []
        self._playing_ids = []
        self._current_player_id = 0
        self._endgame_score = endgame_score
        self._current_observation = {}

    def get_observation(self):
        ob = {}
        ob['scores'] = [player.get_score() for player in self._players]
        ob['playing_cards'] = self._playing_cards.copy()
        ob['playing_ids'] = self._playing_ids.copy()
        ob['hand_cards'] =self._players[self._current_player_id].get_hand_cards()
        if len(self._playing_cards) == 0:
            ob['valid_hand_cards'] = ob['hand_cards']
        else:
            trick_suit = Card.get_suit_int(self._playing_cards[0])
            ob['valid_hand_cards'] = [card for card in ob['hand_cards'] if Card.get_suit_int(card) == trick_suit]
            if len(ob['valid_hand_cards']) == 0:
                ob['valid_hand_cards'] = ob['hand_cards']
        return ob

    def add_player(self, strategy):
        player_id = len(self._players)
        player = Player(player_id, strategy)
        self._players.append(player)

    def start(self):
        if self._trick == 0 and self._round == 0:
            self._number_of_players = len(self._players)
            self._number_of_hand_card_per_player = 52 // self._number_of_players
            self._start_new_round()

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
        rewards = [0] * self._number_of_players
        info = {}
        if len(self._playing_cards) == self._number_of_players:
            self._current_player_id = punish_player_id
            rewards[punish_player_id] = punish_score
        else:
            self._current_player_id += 1
            self._current_player_id = self._current_player_id % 4
        done = False
        if self._trick == self._number_of_hand_card_per_player:
            scores = [player.get_score() for player in self._players]
            for score in scores:
                if score >= 100:
                    done = True
                    break
            if done is False:
                self._start_new_round()
        observation = self.get_observation()
        self._current_observation = observation
        return observation, rewards, done, info

    def move(self):
        return self._players[self._current_player_id].move(self._current_observation)

    def _start_new_round(self):
        self._deck = Deck()
        self._deck.shuffle()
        for player in self._players:
            player.reset_hand_cards(self._deck.draw(self._number_of_hand_card_per_player))
        self._trick = 0
        self._playing_cards = []
        self._playing_ids = []
        self._current_player_id = 0
        self._round += 1
        self._current_observation = self.get_observation()

    def reset(self):
        self._deck = Deck()
        self._deck.shuffle()
        for player in self._players:
            player.reset(self._deck.draw(self._number_of_hand_card_per_player))
        self._trick = 0
        self._playing_cards = []
        self._playing_ids = []
        self._current_player_id = 0
        self._round = 0

    def render(self, mode='human', close=False):
        print("-------PLAYER------")
        for i in range(self._number_of_players):
            print("player {}".format(i))
            Card.print_pretty_cards(self._players[i].get_hand_cards())
            print("score: {}".format(self._players[i].get_score()))
        print("--------BOARD-------")
        Card.print_pretty_cards(self._playing_cards)
        print("--------------------")
