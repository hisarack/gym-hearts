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
        self._shooting_the_moon_enabled = False

    def enable_shooting_the_moon(self):
        self._shooting_the_moon_enabled = True

    def get_observation(self):
        ob = {}
        ob['trick'] = self._trick
        ob['round'] = self._round
        ob['number_of_players'] = self._number_of_players
        ob['scores'] = [player.get_score() for player in self._players]
        ob['playing_cards'] = self._playing_cards.copy()
        ob['playing_ids'] = self._playing_ids.copy()
        ob['hand_cards'] = self._players[self._current_player_id].get_hand_cards()
        ob['current_player_id'] = self._current_player_id
        if len(self._playing_cards) == 0:
            ob['valid_hand_cards'] = ob['hand_cards']
        else:
            trick_suit = Card.get_suit_int(self._playing_cards[0])
            ob['valid_hand_cards'] = [card for card in ob['hand_cards'] if Card.get_suit_int(card) == trick_suit]
            if len(ob['valid_hand_cards']) == 0:
                ob['valid_hand_cards'] = ob['hand_cards']
        ob['number_of_hand_cards_for_all_players'] = [len(player.get_hand_cards()) for player in self._players]
        return ob

    def add_player(self, strategy, hand_cards=None):
        player_id = len(self._players)
        player = Player(player_id, strategy)
        if hand_cards is not None:
            player.reset_hand_cards(hand_cards)
        self._players.append(player)

    def copy_observation(self, observation):
        ob = observation
        self._number_of_players = ob['number_of_players']
        self._number_of_hand_card_per_player = 52 // self._number_of_players
        self._trick = ob['trick']
        self._round = ob['round']
        self._playing_cards = ob['playing_cards'].copy()
        self._playing_ids = ob['playing_ids'].copy()
        self._current_player_id = ob['current_player_id']
        self._current_observation = self.get_observation()

    def start(self):
        if self._trick == 0 and self._round == 0:
            self._number_of_players = len(self._players)
            self._number_of_hand_card_per_player = 52 // self._number_of_players
            self._start_new_round()

    def step(self, action_card):
        info = {}
        info['current_player_id'] = self._current_player_id
        info['action'] = action_card
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
            info['punish_score'] = punish_score
            info['punish_player_id'] = punish_player_id
        rewards = [0] * self._number_of_players
        if len(self._playing_cards) == self._number_of_players:
            self._current_player_id = punish_player_id
            rewards[punish_player_id] = punish_score
        else:
            self._current_player_id += 1
            self._current_player_id = self._current_player_id % 4
        done = False
        is_new_round = False
        if self._trick == self._number_of_hand_card_per_player:
            scores = [player.get_score() for player in self._players]
            for score in scores:
                if score >= 100:
                    done = True
                    break
            if done is False:
                self._start_new_round()
                is_new_round = True
        info['is_new_round'] = is_new_round
        info['done'] = done
        if is_new_round or done:
            if self._shooting_the_moon_enabled is True:
                self._evaluator.shooting_the_moon(self._players)
            for player in self._players:
                player.commit_new_round_score()
        observation = self.get_observation()
        self._current_observation = observation
        self._players_watch(info)
        return observation, rewards, done, info

    def _players_watch(self, info):
        for player in self._players:
            player._watch(self._current_observation, info)

    def move(self):
        if len(self._current_observation['playing_cards']) == 4:
            self._current_observation['playing_cards'].clear()
            self._current_observation['playing_ids'].clear()
        return self._players[self._current_player_id].move(self._current_observation)

    def _start_new_round(self):
        deck = Deck()
        deck.shuffle()
        for player in self._players:
            player.reset_hand_cards(deck.draw(self._number_of_hand_card_per_player))
        self._trick = 0
        self._playing_cards = []
        self._playing_ids = []
        self._current_player_id = 0
        self._round += 1
        self._current_observation = self.get_observation()

    def reset(self):
        deck = Deck()
        deck.shuffle()
        for player in self._players:
            player.reset(deck.draw(self._number_of_hand_card_per_player))
        self._trick = 0
        self._playing_cards = []
        self._playing_ids = []
        self._current_player_id = 0
        self._round = 0

    def render(self):
        print("--------GAME-------")
        print("round: {}".format(self._round))
        print("trick: {}".format(self._trick))
        print("-------PLAYER------")
        for i in range(self._number_of_players):
            print("player {}".format(i))
            playing_cards = [Card.int_to_pretty_str(c) for c in self._players[i].get_hand_cards(is_sorted=True)]
            print(' '.join(playing_cards))
            print("score: {}".format(self._players[i].get_score()))
        print("--------BOARD-------")
        playing_card_strs = ["[]"] * self._number_of_players
        for playing_id, playing_card in zip(self._playing_ids, self._playing_cards):
            playing_card_strs[playing_id] = Card.int_to_pretty_str(playing_card)
        print(' '.join(playing_card_strs))
        print("--------------------")
        print("")
